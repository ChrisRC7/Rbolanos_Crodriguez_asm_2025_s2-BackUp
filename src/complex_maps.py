import numpy as np

# ---------------- Mapeos Complejos ----------------
def linear_complex_map(z, a=1+0.5j, b=0.1+0.1j):
    """
    The function linear_complex_map applies a linear transformation to a complex number z using the
    parameters a and b.
    
    :param z: The `z` parameter in the `linear_complex_map` function represents a complex number that
    will be used in the linear transformation calculation
    :param a: The parameter `a` is a complex number with a real part of 1 and an imaginary part of 0.5
    :param b: The parameter `b` in the `linear_complex_map` function is a complex number with a real
    part of 0.1 and an imaginary part of 0.1. It is used as part of the linear transformation applied to
    the input complex number `z`
    :return: The function `linear_complex_map` takes a complex number `z` as input and returns the
    result of the linear complex map operation, which is given by the formula `a * z + b`, where `a` and
    `b` are complex numbers with default values `a=1+0.5j` and `b=0.1+0.1j`.
    """
    return a * z + b

def inverse_complex_map(z, epsilon=1e-5):
    """
    The function `inverse_complex_map` calculates the inverse of a complex number with a small offset to
    avoid division by zero.
    
    :param z: The `z` parameter in the `inverse_complex_map` function is a complex number. It is the
    input value for which we want to calculate the inverse
    :param epsilon: The `epsilon` parameter in the `inverse_complex_map` function is a small positive
    value used to avoid division by zero errors when the absolute value of the complex number `z` is
    very close to zero. If the absolute value of `z` is less than `epsilon`, `z_safe`
    :return: The function `inverse_complex_map` returns the inverse of the input complex number `z`,
    with a small epsilon value added to avoid division by zero errors.
    """
    z_safe = np.where(np.abs(z) < epsilon, epsilon, z)
    return 1 / z_safe

def bilinear_complex_map(z, a=1, b=0.5, c=0.2, d=1):
    numerator = a * z + b
    denominator = c * z + d
    denominator = np.where(np.abs(denominator) < 1e-5, 1e-5, denominator)
    return numerator / denominator

def exponential_complex_map(z, scale=1):
    return np.exp(scale * z)

def quadratic_complex_map(z, a=1, b=0, c=0):
    return a * z**2 + b * z + c

def cascade_complex_map(z):
    w = quadratic_complex_map(z, 0.8, 0.2j, 0.1)
    w = linear_complex_map(w, 0.9+0.1j, 0.05)
    w = bilinear_complex_map(w, 1, 0.3j, 0.1, 1)
    return w
