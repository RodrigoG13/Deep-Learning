import numpy as np

def tanh(h:np.float64):
    """
    Compute the hyperbolic tangent for h.

    Parameters:
    h (numpy.float64): Input number.

    Returns:
    numpy.np.float64: Hyperbolic tangent evaluation
    """
    return np.tanh(h)

print(tanh(12.7))