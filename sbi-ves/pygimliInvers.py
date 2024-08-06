from pygimli.physics import VESManager
import numpy as np

class PyGimliInversion:

    def __init__ (self, num_measurements, ab2, mn2=1, error=0.03):
        self.num_measurements = num_measurements
        self.ab2 = ab2
        self.mn2=mn2
        self.error = error
        
        

    def invert(self, app_res, num_layers): 
        err = np.repeat(self.error, self.num_measurements)
        ves = VESManager()
        ves.invert(data=app_res,
                   relativeError=err,
                   ab2=self.ab2,
                   mn2=np.repeat(self.mn2, self.num_measurements),
                   nLayers=num_layers,
                   lam=1000,
                   lamdaFactor=0.8
                   )
        return ves.model, ves.inv.response
        