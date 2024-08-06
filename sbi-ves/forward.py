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


class Forward:

    def __init__(self, thicknesses, survey):
        self.thicknesses = thicknesses
        self.survey = survey

    # Helper functions to add noise 

    
    def add_relative_noise(self, apparent_resistivities, var=0.05):
        '''
        Add relative gaussian distributed noise to the apparent resistivity signal, with variance of 0.05 * the app.res signal.  
        '''
        # Ensure we are working with numpy array
        apparent_resistivities = np.array(apparent_resistivities)
    
        # Generate noise
        noise = np.random.normal(loc=0, scale=apparent_resistivities * var, size=apparent_resistivities.shape)
        
        return np.maximum(0.0, apparent_resistivities + noise)
    
    def add_absolute_noise(self, apparent_resistivities, noise_level):
        '''
        Add white noise according to white noise level to the the apparent resistivity signal.  
        '''
        # Ensure we are working with numpy array
        apparent_resistivities = np.array(apparent_resistivities)
    
        # Generate noise from uniform distribution
        noise = np.random.uniform(low=-noise_level, high=noise_level, size=apparent_resistivities.shape)
        
        return np.maximum(0.0, apparent_resistivities + noise)

    
    # Note parameters are composed of resistivities and thicknesses - in that order. First resistivities then thicknesses
    def dc_forward_model(self, resistivities):
        '''
        Forward simulations with SimPEG. 
        Given the input resistivities and the class inherent layer thicknesses, the forward simulator of SimPEG is evaluated and returns the apparent resistivity signal of that depth profile.

        Returns simulated apparent resistivity given resistivity values and layer thicknesses. 
        '''
        # Define mapping from model to 1D layers.
        model_map = maps.IdentityMap(nP=len(resistivities))
        # SimPegs 1D Simulation
        simulation = dc.simulation_1d.Simulation1DLayers(
            survey=self.survey,
            rhoMap=model_map,
            thicknesses=self.thicknesses,
        )

        # Predict data for a given model
        return simulation.dpred(resistivities)

    def dc_forward_model_base_noise(self, resistivities, noise_level):
        '''
        Forward simulations with SimPEG. 
        Given the input resistivities and the class inherent layer thicknesses, the forward simulator of SimPEG is evaluated and returns the apparent resistivity signal of that depth profile.
        White noise with given noise_level is added to the apparent resistivity signal. 

        Returns noisy simulated apparent resistivity given resistivity values and layer thicknesses. 
        '''
        apparent_resistivity = self.dc_forward_model(resistivities)
        return self.add_absolute_noise(apparent_resistivity, noise_level=noise_level)
