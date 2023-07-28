"""
Mathematical functions used in all submodules.
"""

import numpy as np
from xhistogram.core import histogram

# #### Trigo functions in degree #


def tand(x):
    """Compute tangent element-wise using :func:`np.tan <numpy.tan>` with an input in degree.

    Parameters
    ----------
    x : array_like
        Input array in degree.

    Returns
    -------
    y : array_like
        The corresponding tangent values. This is a scalar if x is a scalar.

    """
    return np.tan(np.radians(x))


def sind(x):
    """Trigonometric sine using :func:`np.sin <numpy.sin>`, element-wise with an input in degree.

    Parameters
    ----------
    x : array_like
        Input array in degree.

    Returns
    -------
    y : array_like
        The corresponding tangent values. This is a scalar if x is a scalar.

    """
    return np.sin(np.radians(x))


def cosd(x):
    """Cosine element-wise :func:`np.cos <numpy.cos>` with an input in degree.

    Parameters
    ----------
    x : array_like
        Input array in degree.

    Returns
    -------
    y : array_like
        The corresponding tangent values. This is a scalar if x is a scalar.

    """
    return np.cos(np.radians(x))


def arctand(x):
    """Trigonometric inverse tangent using :func:`np.arctan <numpy.arctan>`, element-wise with an output in degree.

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    y : array_like
        The corresponding tangent values. This is a scalar if x is a scalar.

    """
    return np.degrees(np.arctan(x))


def arcsind(x):
    """Trigonometric inverse sine using :func:`np.arcsine <numpy.arctan>`, element-wise with an output in degree.

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    y : array_like
        The corresponding tangent values. This is a scalar if x is a scalar.

    """
    return np.degrees(np.arcsin(x))


def arctan2d(x1, x2):
    """Element-wise arc tangent of x1/x2 choosing the quadrant correctly using :func:`np.arctan2 <numpy.arctan2>` with an output in degree.

    Parameters
    ----------
    x1 : array_like, real-valued
        y-coordinates.
    x2 : array_like, real-valued
        x-coordinates. If x1.shape != x2.shape, they must be broadcastable to a common shape (which becomes the shape of the output).

    Returns
    -------
    angle : array_like
        Array of angles in degrees, in the range [-180, 180]. This is a scalar if both x1 and x2 are scalars.

    """
    return np.degrees(np.arctan2(x1, x2))


# #### Other functions

def vector_average(angles, norm, axis=-1):
    """Calculate the average vector from series of angles and norms.

    Parameters
    ----------
    angles : array_like
        angles.
    norm : array_like
        norms.
    axis : None or int
        axis along wich the averaging is performed (the default is -1). None compute the average on the flattened array.

    Returns
    -------
    angle : array_like
        the counterclockwise angle of the resultant vector in the range [-180, 180].
    norm : array_like
        norm of the resultant vector.

    """
    average = np.nanmean(norm*np.exp(1j*np.radians(angles)), axis=axis)
    return np.degrees(np.angle(average)), np.absolute(average)


def cartesian_to_polar(x, y):
    """make the transformation from cartesian to polar coordinates.

    Parameters
    ----------
    x : array_like
        x-coordinate.
    y : array_like
        y-coordinate.

    Returns
    -------
    r: array_like
        radius coordinate.
    theta: array_like
        angle coordinate, in degree in the range [0, 360].

    """
    r = np.sqrt(x**2 + y**2)
    theta = arctan2d(y, x) % 360
    return r, theta


def make_angular_PDF(angles, weight, bin_edges=np.linspace(0, 360, 361), axis=-1):
    """Calculate the angular PDF (normalized) from input arrays.

    Parameters
    ----------
    angles : np.array
        array of angles.
    weight : np.array
        array of weights. Its dimensions must match those of angles.
    bin_edges : np.array
        array containing the bins used to calculate the distribution (the default is np.linspace(0, 360, 361)).
    axis : int
        axis of the input aray along which the distribution is calculated (the default is -1).

    Returns
    -------
    hist: np.array
        array containing the distribution.
    bin_centers: np.array
        array containing the bin centers of the distribution.

    """
    hist, _ = histogram(angles, bins=bin_edges, density=1, weights=weight, axis=axis)
    bin_centers = bin_edges[1:] - (bin_edges[1] - bin_edges[0])/2
    return hist, bin_centers


def make_angular_average(angles, weight, bin_edges=np.linspace(0, 360, 361), axis=-1):
    """Calculate the average by angle bins from input arrays.

    Parameters
    ----------
    angles : np.array
        array of angles.
    weight : np.array
        array of weights. Its dimensions must match those of angles.
    bin_edges : np.array
        array containing the bins used to calculate the distribution (the default is np.linspace(0, 360, 361)).
    axis : int
        axis of the input aray along which the distribution is calculated (the default is -1).

    Returns
    -------
    hist: np.array
        array containing the averages.
    bin_centers: np.array
        array containing the bin centers.

    """
    hist, _ = histogram(angles, bins=bin_edges, weights=weight, axis=axis)
    counts, _ = histogram(angles, bins=bin_edges, axis=axis)
    bin_centers = np.array([np.mean(bin_edges[i:i+2]) for i in range(bin_edges.size - 1)])
    hist[counts == 0] = 1
    counts[counts == 0] = 1
    return hist/counts, bin_centers
