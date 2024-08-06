import numpy as np

from SimPEG import (
    maps,
    data,
    data_misfit,
    regularization,
    optimization,
    inverse_problem,
    inversion,
    directives,
    utils,
)

from SimPEG.electromagnetics.static import resistivity as dc
from SimPEG.utils import plot_1d_layer_model
from discretize import TensorMesh


class Survey:
    def __init__(self, num_measurements, min_ab_distance=1, max_ab_distance=250, spacing='log'):
        self.num_measurements = num_measurements
        self.min_ab_distance = min_ab_distance
        self.max_ab_distance = max_ab_distance
        self.spacing = spacing

    def schlumberger_survey(self):
        # Define the Schlumberger array configuration for which the measurements measurements for each reading
        if self.spacing == 'log':
            a_b_electrode_separations = np.logspace(np.log10(self.min_ab_distance), np.log10(self.max_ab_distance),
                                                    self.num_measurements)
            m_n_electrode_separations = 0.01 * a_b_electrode_separations
        elif self.spacing == 'lin':
            a_b_electrode_separations = np.linspace(self.min_ab_distance, self.max_ab_distance, self.num_measurements)
            m_n_electrode_separations = 0.01 * a_b_electrode_separations
        else:
            raise Exception('Invalid Spacing - needs to be a string of either "log" or "lin" but it was given', self.spacing)

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
