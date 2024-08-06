import torch
from torch.distributions import Distribution, Uniform, Normal


class CustomDistribution(Distribution):
    def __init__(self, low=1, high=1000, dimension=5, variance=0.05):
        super().__init__()
        self.low = low
        self.high = high
        self.var = variance
        self.dimension = dimension
        self.uniform = Uniform(low, high)


    def sample(self, sample_shape=torch.Size()):
        # Sample from the first dimension (uniform distribution)
        first_dimension = self.uniform.sample(sample_shape)

        # Initialize an empty tensor to store the sampled values
        sampled_values = torch.empty(sample_shape + torch.Size([self.dimension]))

        # Set the first dimension values
        sampled_values[..., 0] = first_dimension

        # Sample the remaining dimensions based on the previous dimension
        for i in range(1, self.dimension):
            # Mean is set to the value of the previous dimension
            mean = sampled_values[..., i - 1]
            # Use a normal distribution for the current dimension
            normal_distribution = Normal(mean, (self.var * self.high))  # You can adjust the scale if needed
            sampled_values[..., i] = torch.clamp(normal_distribution.sample(), min=self.low, max=self.high)

        return sampled_values

    def log_prob(self, value):
        # Compute the log probability of the sampled values

        # Log probability of the first dimension (uniform distribution)
        log_prob_first_dimension = self.uniform.log_prob(value[..., 0])

        # Log probability of the remaining dimensions (normal distribution)
        log_prob_remaining_dimensions = torch.zeros_like(log_prob_first_dimension)

        for i in range(1, self.dimension):
            # Mean is set to the value of the previous dimension
            mean = value[..., i - 1]
            # Use a normal distribution for the current dimension
            normal_distribution = Normal(mean, (self.var * self.high))
            log_prob_remaining_dimensions += normal_distribution.log_prob(value[..., i]) 

        # Sum the log probabilities for all dimensions
        log_prob_total = log_prob_first_dimension + log_prob_remaining_dimensions

        return log_prob_total

    @property
    def batch_shape(self):
        # Assuming no batch dimensions for simplicity
        return torch.Size()