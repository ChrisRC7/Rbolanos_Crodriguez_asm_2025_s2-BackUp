import numpy as np


def create_complex_circle(n_points=256, r=1, center=0+0j):
    theta = np.linspace(0, 2*np.pi, n_points)
    return center + r * np.exp(1j*theta)



def create_complex_line_parametric(z0, w, n_points=1000, t_min=-100, t_max=100):
    """
    Crea puntos para una recta compleja usando la forma paramétrica z(t) = z₀ + tw.
    
    :param z0: Punto de inicio de la recta (número complejo).
    :param w: Vector de dirección de la recta (número complejo).
    :param t_min: Valor mínimo del parámetro t.
    :param t_max: Valor máximo del parámetro t.
    """
    t = np.linspace(t_min, t_max, n_points)
    return z0 + t * w

"""
def create_complex_square(size=256, side=1.5, center=0+0j):
    Z = create_complex_plane(size)
    x, y = np.real(Z), np.imag(Z)
    x0, y0 = np.real(center), np.imag(center)
    half_side = side / 2
    mask = (np.abs(x - x0) <= half_side) & (np.abs(y - y0) <= half_side)
    square = np.zeros((size, size), dtype=complex)
    square[mask] = Z[mask]
    return square

def create_complex_triangle(size=256, vertices=None):
    Z = create_complex_plane(size)
    if vertices is None:
        vertices = np.array([[0,1], [-np.sqrt(3)/2,-0.5],[np.sqrt(3)/2,-0.5]])

    def point_in_triangle(p, v):
        a, b, c = v[0], v[1], v[2]
        v0 = c - a; v1 = b - a; v2 = p - a
        dot00 = np.dot(v0, v0); dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2); dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)
        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11*dot02 - dot01*dot12) * inv_denom
        v = (dot00*dot12 - dot01*dot02) * inv_denom
        return (u >= 0) & (v >= 0) & (u + v <= 1)

    triangle = np.zeros((size, size), dtype=complex)
    for i in range(size):
        for j in range(size):
            point = np.array([np.real(Z[i,j]), np.imag(Z[i,j])])
            if point_in_triangle(point, vertices):
                triangle[i,j] = Z[i,j]
    return triangle
    """