import numpy as np


class Polynomial:
    def __init__(self, max_depth, num_dim, max_res, num_measurements):
        self.max_depth = max_depth
        self.num_dim = num_dim
        self.max_res = max_res
        self.num_measurements = num_measurements

    

    def normalize(self):
        '''
        Helper function to normalize the depth profile, such that it is transformed to the interval [-1,1]
        '''
        depths = np.linspace(0, self.max_depth, num=self.num_dim)
        half_max_depth = self.max_depth/2
        return (depths - half_max_depth)/half_max_depth

    
    
    # Legendre Polynomial function
    def legendre_polynomial(self, x, coefficients):
        '''
        For given coefficients (from the prior or posterior) generate the Polynomial function that is composed of the first five Legendre Polynomials, given the coefficients.  
        The polynomial is evaluated on the points described in x.
        
        Returns the values at x of the generated polynomial function.
        '''
        poly = np.polynomial.legendre.Legendre(coefficients)
        return poly(x)
    
    def legendre_polynomial_nan(self, coefficients): 
        '''
        For given coefficients (from the prior or posterior) generate the Polynomial function that is composed of the first five Legendre Polynomials, given the coefficients.  
        The polynomial is evaluated on the points described in x.
        If the polynomial exceeds the range of [-1,1] under which Legendre polynomials are well-defined, an array of nan-values is returned, to mark this sample as invalid. 
        
        Returns the values at x of the generated polynomial function.
        '''
        normalized_depth = self.normalize()
        
        coefficients = coefficients
        poly = self.legendre_polynomial(normalized_depth, coefficients)
        if np.any((poly < -1) | (poly > 1)):
            return np.full((normalized_depth.shape[0],), np.nan)
        else: 
            return poly
    
    def poly_to_resistivity(self, poly): 
        '''
        Transforms the polynomial values from the interval of [-1,1] to the interval [0 - max_res]
        '''
        
        return (poly + 1) * (self.max_res/2)


    def coefficients_to_resistivity(self, coeff):
        '''
        For a sample of coefficients, the Legendre Polynomial is generated. 
        If the sample is valid (not exceeding the range of [-1,1]) the values are transformed to the resistivity interval. 
        '''
        
        poly = self.legendre_polynomial_nan(coeff)
        if np.isnan(poly).all():
            return np.full((self.num_dim,), np.nan)
        else: 
            return self.poly_to_resistivity(poly)