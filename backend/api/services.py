# services.py
import os
import pickle
import torch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from uuid import UUID
from flask import jsonify

from SimPEG import maps
from SimPEG.electromagnetics.static import resistivity as dc

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from sbi.utils import user_input_checks as uic

from . import db, app
from .models import User, Measurement, File


class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(userId):
        user = User.query.get(userId)
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        return user

    @staticmethod
    def get_user_by_username(username):
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        return user

    @classmethod
    def create_user(cls, data):
        user = User(**data)
        return cls.save_user(user)

    @classmethod
    def save_user(cls, user):
        db.session.add(user)
        db.session.commit()
        return user


class MeasurementService:
    @classmethod
    def save_measurement(cls, measurement):
        db.session.add(measurement)
        db.session.commit()
        return measurement

    @classmethod
    def map_to_measurement(cls, measurementDto, file, saved_file):
        # Map the data sent in the measurementDto such as location, date and comment
        mapped_measurement = Measurement(**measurementDto)
        # Link the measurement to the file that was saved
        mapped_measurement.fileId = saved_file.id
        # Parse the measurement values from the file
        measurements_from_file = FileService.parse_measurements_from_file(file, saved_file)

        # List of attribute names in the same order as the values in measurements_from_file
        attributes = [
            'ab2_2', 'ab2_2_5', 'ab2_3', 'ab2_3_6', 'ab2_4_4', 'ab2_5_2', 'ab2_6_3',
            'ab2_7_5', 'ab2_8_7', 'ab2_10', 'ab2_12', 'ab2_14_5', 'ab2_17_5', 'ab2_21',
            'ab2_25', 'ab2_30', 'ab2_36', 'ab2_44', 'ab2_52', 'ab2_63', 'ab2_75', 'ab2_87', 'ab2_100'
        ]

        # Link each attribute name with its corresponding value
        for attr, value in zip(attributes, measurements_from_file):
            setattr(mapped_measurement, attr, value)

        return mapped_measurement

    @staticmethod
    def get_measurement_by_id(measurementId):
        measurement = Measurement.query.get(measurementId)
        if measurement is None:
            return jsonify({'error': 'Measurement not found'}), 404
        return measurement


class FileService:

    @classmethod
    def save_file_in_db(cls, file):
        db.session.add(file)
        db.session.commit()
        return file

    @classmethod
    def save_file_locally(cls, file):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename))
        print('File successfully saved locally')
        return file.filename

    @classmethod
    def create_file_from_upload(cls, uploaded_file: FileStorage, user_id: UUID):
        # Extract necessary information from the uploaded file
        fileName = secure_filename(uploaded_file.filename)
        file_extension = os.path.splitext(fileName)[1]
        file_size = uploaded_file.content_length

        # Create a new instance of the File class
        new_file = File(
            userId=user_id,
            fileName=fileName,
            fileExtension=file_extension,
            fileSize=file_size
        )

        return new_file

    @classmethod
    def parse_measurements_from_file(cls, file, saved_file):
        if saved_file.fileExtension == '.csv':
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Replace NaN values with None
        # df = df.where(pd.notnull(df), None)

        # Extract the measurement values
        measurements = df.iloc[:, 1].values

        return measurements


class InversionService:
    max_depth = 20
    num_points = 40
    degree = 5
    step_size = 0.5
    max_coefficient = 500
    min_coefficient = -500

    # Define survey setup - measurement points and distance
    num_measurements = 23
    max_spacing = 100

    attributes = [
        'ab2_2', 'ab2_2_5', 'ab2_3', 'ab2_3_6', 'ab2_4_4', 'ab2_5_2', 'ab2_6_3',
        'ab2_7_5', 'ab2_8_7', 'ab2_10', 'ab2_12', 'ab2_14_5', 'ab2_17_5', 'ab2_21',
        'ab2_25', 'ab2_30', 'ab2_36', 'ab2_44', 'ab2_52', 'ab2_63', 'ab2_75', 'ab2_87', 'ab2_100'
    ]

    ab2_electrode_spacing = [2, 2.5, 3, 3.6, 4.4, 5.2, 6.3, 7.5, 8.7, 10, 12, 14.5, 17.5, 21, 25, 30, 36, 44, 52, 63,
                             75, 87, 100]

    # Define the depth profile with 40steps each of 0.5m depth
    depths = np.arange(0, max_depth, step_size)
    thicknesses = torch.ones(num_points) * 0.5

    colors = ['navy', 'cornflowerblue', 'skyblue']
    percentiles = [5, 10, 20, 80, 90, 95]

    @classmethod
    def normalize_depth(cls, depths, max_depth):
        half_max_depth = max_depth / 2
        return (depths - half_max_depth) / half_max_depth

    @classmethod
    def unpickle(cls, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    @classmethod
    def get_posterior(cls, type):
        if type == 'step':
            inference_step, posterior_step = cls.unpickle('./api/posterior_models/steps_for_terrana_survey_100k.pkl')
            return posterior_step
        if type == 'polynom':
            _, posterior_poly = cls.unpickle('./api/posterior_models/legendre_for_terrana_survey_100k.pkl')
            return posterior_poly

    @classmethod
    def invert_measurement(cls, measurement, modelType):
        # Get the values of the attributes from measurement
        app_res = [getattr(measurement, attr) for attr in cls.attributes]
        posterior = cls.get_posterior(modelType)
        posterior.set_default_x(app_res)
        posterior_samples = posterior.sample((100_000,))
        print('Compute log probs ...')
        log_probs = posterior.log_prob(posterior_samples)
        sorted_log_probs = torch.argsort(log_probs)
        print('Log probs Computed!')
        filename = './api/upload/files/{0}-{1}-inversion.png'.format(modelType, measurement.id)
        if modelType == 'polynom':
            # return cls.generate_poly_figure_with_subplots(app_res, posterior_samples, sorted_log_probs, filename)
            return cls.generate_poly_figure_with_uncertainties(app_res, posterior_samples, sorted_log_probs, filename)
        elif modelType == 'step':
            return cls.generate_step_figure_with_uncertainties(app_res, posterior_samples, sorted_log_probs, filename)

    @classmethod
    def generate_poly_figure_with_subplots(cls, app_res, posterior_samples, sorted_log_probs, filename):
        normalized_depth = cls.normalize_depth(cls.depths, cls.max_depth)  # Normalize the same depth between [-1,1]

        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(16, 12))

        for index in sorted_log_probs[-50:]:
            posterior_sample = posterior_samples[index]
            res = ForwardModelService.legendre_polynomial(normalized_depth, posterior_sample * cls.max_coefficient)
            ax1.plot(res, cls.depths, color='#ff7f0e', alpha=0.3)

            app_resistivity = ForwardModelService.legendre_forward_nan_noise_5(np.array(posterior_sample))
            ax2.plot(app_resistivity, cls.ab2_electrode_spacing, color='#ff7f0e', alpha=0.3)

        ax1.plot([], [], label='Posterior Samples')
        ax1.invert_yaxis()
        ax1.set_xlabel("Resistivity")
        ax1.set_ylabel("Depth (m)")
        ax1.set_title("Resistivity Profile in Subsurface")
        ax1.grid(True)

        ax2.plot(app_res, cls.ab2_electrode_spacing, marker='x', label="True Sounding Curve")

        ax2.plot([], [], label='Posterior Samples')
        ax2.invert_yaxis()
        ax2.set_yscale('log')
        ax2.set_xlabel(r"Apparent Resistivity ($\Omega m$)")
        ax2.set_ylabel("AB/2 (m)")
        ax2.legend()

        plt.savefig(filename)
        return filename.replace('api/', '')

    @classmethod
    def generate_poly_figure_with_uncertainties(cls, app_res, posterior_samples, sorted_log_probs, filename):
        normalized_depth = cls.normalize_depth(cls.depths, cls.max_depth)  # Normalize the same depth between [-1,1]

        resistivities_leg = []
        apparent_resistivities_leg = []

        print("Compute apparent resistivities from posterior samples")
        for index in reversed(sorted_log_probs):
            posterior_sample = posterior_samples[index]
            res = ForwardModelService.legendre_polynomial(normalized_depth, posterior_sample * cls.max_coefficient)
            resistivities_leg.append(res)
            app_resistivity = ForwardModelService.legendre_forward_nan_noise_5(np.array(posterior_sample))
            if not np.any(np.isnan(app_resistivity)):
                apparent_resistivities_leg.append(app_resistivity)

            if len(apparent_resistivities_leg) >= 100:
                break
        print("Apparent resistivities from posterior samples computed!")
        mean_res = np.mean(resistivities_leg, axis=0)
        mean_ar = np.nanmean(apparent_resistivities_leg, axis=0)
        # Compute confidence intervals for resistivity
        conf_intervals_res = np.percentile(resistivities_leg, q=cls.percentiles, axis=0)

        # Compute confidence intervals for apparent resistivity
        conf_intervals_ar = np.percentile(apparent_resistivities_leg, q=cls.percentiles, axis=0)

        # Plotting
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(16, 12))

        # Plot resistivity
        ax1.plot(mean_res, cls.depths, label='Mean', marker='_')

        for idx, percentile in enumerate(cls.percentiles[3:]):
            ax1.fill_betweenx(cls.depths, conf_intervals_res[3 + idx], conf_intervals_res[2 - idx], alpha=0.4,
                              color=cls.colors[idx], label=f'{cls.percentiles[3 + idx]}% CI')

        ax1.set_xlabel("Resistivity")
        ax1.set_ylabel("Depth (m)")
        ax1.set_title("Resistivity Profile in Subsurface")
        ax1.legend()
        ax1.grid(True)
        ax1.invert_yaxis()

        # Plot mean apparent resistivity
        ax2.plot(mean_ar, cls.ab2_electrode_spacing, label='Mean')

        # Plot measurement
        ax2.plot(app_res, cls.ab2_electrode_spacing, marker='x', color='gray', label="Measurement")

        for idx, percentile in enumerate(cls.percentiles[3:]):
            ax2.fill_betweenx(cls.ab2_electrode_spacing, conf_intervals_ar[3 + idx], conf_intervals_ar[2 - idx],
                              alpha=0.4,
                              color=cls.colors[idx], label=f'{cls.percentiles[3 + idx]}% CI')
        ax2.set_title('Apparent Resistivity from Posterior Samples')
        ax2.set_xlabel(r"Apparent Resistivity ($\Omega m$)")
        ax2.set_ylabel("AB/2 (m)")
        ax2.set_yscale('log')
        ax2.legend()
        ax2.invert_yaxis()
        ax2.grid(True)

        plt.savefig(filename)
        return filename.replace('api/', '')

    @classmethod
    def generate_step_figure_with_uncertainties(cls, app_res, posterior_samples, sorted_log_probs, filename):
        resistivities_step = []
        apparent_resistivities_step = []

        print("Compute apparent resistivities from posterior samples")
        for index in reversed(sorted_log_probs):
            # Sample a random value within the length of posterior_samples
            res = posterior_samples[index]
            resistivities_step.append(res)
            app_resistivity = ForwardModelService.steps_forward_model_base_noise_5(np.array(res))
            if not np.any(np.isnan(app_resistivity)):
                apparent_resistivities_step.append(app_resistivity)

            if len(apparent_resistivities_step) >= 100:
                break
        print("Apparent resistivities from posterior samples computed!")
        mean = np.mean(resistivities_step, axis=0)
        mean_ar = np.mean(apparent_resistivities_step, axis=0)
        # Compute confidence intervals for resistivity
        conf_intervals_res = np.percentile(resistivities_step, q=cls.percentiles, axis=0)

        # Compute confidence intervals for apparent resistivity
        conf_intervals_ar = np.percentile(apparent_resistivities_step, q=cls.percentiles, axis=0)

        # Plotting
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(16, 12))

        # Plot the mean line
        ax1.plot(mean, cls.depths, label='Mean', drawstyle='steps-mid')

        for idx, percentile in enumerate(cls.percentiles[3:]):
            ax1.fill_betweenx(cls.depths, conf_intervals_res[3 + idx], conf_intervals_res[2 - idx], alpha=0.4,
                              color=cls.colors[idx], label=f'{cls.percentiles[3 + idx]}% CI')
        ax1.set_xlabel("Resistivity")
        ax1.set_ylabel("Depth (m)")
        ax1.set_title("Resistivity Profile in Subsurface")
        ax1.legend()
        ax1.grid(True)
        ax1.invert_yaxis()

        # Plot mean apparent resistivity
        ax2.plot(mean_ar, cls.ab2_electrode_spacing, label='Mean')

        # Plot measurement
        ax2.plot(app_res, cls.ab2_electrode_spacing, marker='x', color='gray', label="Measurement")

        for idx, percentile in enumerate(cls.percentiles[3:]):
            ax2.fill_betweenx(cls.ab2_electrode_spacing, conf_intervals_ar[3 + idx], conf_intervals_ar[2 - idx],
                              alpha=0.4,
                              color=cls.colors[idx], label=f'{cls.percentiles[3 + idx]}% CI')
        ax2.set_title('Apparent Resistivity from Posterior Samples')
        ax2.set_xlabel(r"Apparent Resistivity ($\Omega m$)")
        ax2.set_ylabel("AB/2 (m)")
        ax2.set_yscale('log')
        ax2.legend()
        ax2.invert_yaxis()
        ax2.grid(True)

        plt.savefig(filename)
        return filename.replace('api/', '')


class ForwardModelService:
    max_depth = 20
    step_size = 0.5
    num_points = 40
    max_coefficient = 500
    min_coefficient = -500

    # Define survey setup - measurement points and distance
    num_measurements = 23
    ab2_electrode_spacing = [2, 2.5, 3, 3.6, 4.4, 5.2, 6.3, 7.5, 8.7, 10, 12, 14.5, 17.5, 21, 25, 30, 36, 44, 52, 63,
                             75, 87, 100]

    # Define the depth profile with 40steps each of 0.5m depth
    depths = np.arange(0, max_depth, step_size)
    thicknesses = torch.ones(num_points) * 0.5

    # ***** Universal Functions   **********+***************************
    @classmethod
    def schlumberger_survey(cls, num_measurements, spacing='log'):
        # Define the 'a' spacing for Schlumberger array measurements for each reading
        if spacing == 'log':
            a_b_electrode_separations = np.asfarray(cls.ab2_electrode_spacing)
            m_n_electrode_separations = np.repeat(1.0, num_measurements)
        elif spacing == 'lin':
            a_b_electrode_separations = np.asfarray(cls.ab2_electrode_spacing)
            m_n_electrode_separations = np.repeat(1.0, num_measurements)
        else:
            raise Exception('Invalid Spacing - needs to be a string of either "log" or "lin" but it was given', spacing)

        source_list_log = []  # create empty array for sources to live

        for ab, mn in zip(a_b_electrode_separations, m_n_electrode_separations):
            # AB electrode locations for source. Each is a (1, 3) numpy array
            A_location = np.r_[-ab, 0.0, 0.0]
            B_location = np.r_[ab, 0.0, 0.0]

            # MN electrode locations for receivers. Each is an (N, 3) numpy array
            M_location = np.r_[-mn, 0.0, 0.0]
            N_location = np.r_[mn, 0.0, 0.0]

            # Create receivers list. Define as pole or dipole.
            receiver_list = dc.receivers.Dipole(
                M_location, N_location, data_type="apparent_resistivity"
            )
            receiver_list = [receiver_list]

            # Define the source properties and associated receivers
            source_list_log.append(dc.sources.Dipole(receiver_list, A_location, B_location))

        # Define survey
        survey = dc.Survey(source_list_log)

        electrode_separations = 0.5 * np.sqrt(
            np.sum((survey.locations_a - survey.locations_b) ** 2, axis=1)

        )
        return survey, electrode_separations

    @classmethod
    def dc_forward_model(cls, resistivities, thicknesses):
        survey, electrode_spacing = cls.schlumberger_survey(cls.num_measurements)

        # Define mapping from model to 1D layers.
        model_map = maps.IdentityMap(nP=len(resistivities))
        # SimPegs 1D Simulation
        simulation = dc.simulation_1d.Simulation1DLayers(
            survey=survey,
            rhoMap=model_map,
            thicknesses=thicknesses,
        )

        # Predict data for a given model
        pred = simulation.dpred(resistivities)
        return pred

    @classmethod
    def add_absolute_noise(cls, apparent_resistivities, noise_level):
        # Ensure we are working with numpy array
        apparent_resistivities = np.array(apparent_resistivities)

        # Generate noise from uniform distribution
        noise = np.random.uniform(low=-noise_level, high=noise_level, size=apparent_resistivities.shape)

        return np.maximum(0.0, apparent_resistivities + noise)

    @classmethod
    def dc_forward_model_base_noise(cls, resistivities, thicknesses, noise_level):
        apparent_resistivity = cls.dc_forward_model(resistivities, thicknesses)
        return cls.add_absolute_noise(apparent_resistivity, noise_level=noise_level)

    # **** Polynomial forward model *******************************************
    @classmethod
    def normalize_depth(cls, depths, max_depth):
        half_max_depth = max_depth / 2
        return (depths - half_max_depth) / half_max_depth

    # Helper functions and configurations
    @classmethod
    def legendre_polynomial(cls, x, coefficients):
        poly = np.polynomial.legendre.Legendre(coefficients)
        return poly(x)

    @classmethod
    # Interpolate Legendre polynomial coefficients and remove invalid simulations by substitue with nan values
    def legendre_forward_nan_noise_5(cls, coefficients):
        normalized_depth = cls.normalize_depth(cls.depths, cls.max_depth)  # Normalize the same depth between [-1,1]
        coefficients = coefficients * cls.max_coefficient
        res = cls.legendre_polynomial(normalized_depth, coefficients)
        if (np.any([res < 0])):
            nan_array = np.empty((cls.num_measurements,))
            nan_array[:] = np.nan
            return nan_array
        else:
            return cls.dc_forward_model_base_noise(res, cls.thicknesses, 5)

    # **** Step forward model *******************************************

    @classmethod
    def steps_forward_model_no_noise(cls, res):
        return cls.dc_forward_model(res, cls.thicknesses)

    @classmethod
    def steps_forward_model_base_noise_5(cls, res):
        if (np.any([res < 0])):
            nan_array = np.empty((cls.num_measurements,))
            nan_array[:] = np.nan
            return nan_array
        return cls.dc_forward_model_base_noise(res, cls.thicknesses, 5)
