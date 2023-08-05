# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "29/09/2021"

import numpy
try:
    import tqdm
except ImportError:
    tqdm = None
from functools import partial
import multiprocessing
from multiprocessing import Pool
from scipy.optimize import curve_fit
from scipy.stats import skew, kurtosis
from silx.math.medianfilter import medfilt2d


def gaussian(x, a, b, c, d):
    """
    Function to calculate the Gaussian with constants a, b, and c

    :param float x: Value to evaluate
    :param float a: height of the curve's peak
    :param float b: position of the center of the peak
    :param float c: standard deviation
    :param float d: lowest value of the curve (value of the limits)

    :returns: result of the function on x
    :rtype: float
    """
    return d + a * numpy.exp(-numpy.power(x - b, 2) / (2 * numpy.power(c, 2)))


def multi_gaussian(M, x0, y0, xalpha, yalpha, A, C, bg):
    """
    Bivariate case of the multigaussian PDF + background
    """
    x, y = M
    return bg + A * numpy.exp(-0.5 * (1 - C**2) * (((x - x0) / xalpha)**2 + ((y - y0) / yalpha)**2) + 2 * C * (x - x0) * (y - y0))


def generator(data, moments=None):
    """
    Generator that returns the rocking curve for every pixel

    :param ndarray data: data to analyse
    :param moments: array of same shape as data with the moments values per pixel and image, optional
    :type moments: Union[None, ndarray]
    """
    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            if moments is not None:
                yield data[:, i, j], moments[:, i, j]
            yield data[:, i, j], None


def generator_2d(data, moments=None):
    """
    Generator that returns the rocking curve for every pixel

    :param ndarray data: data to analyse
    :param moments: array of same shape as data with the moments values per pixel and image, optional
    :type moments: Union[None, ndarray]
    """
    for i in range(data.shape[2]):
        for j in range(data.shape[3]):
            yield data[:, :, i, j], None


def fit_rocking_curve(y_values, values=None, num_points=None, int_thresh=None):
    """
    Fit rocking curve.

    :param tuple y_values: the first element is the dependent data and the second element are
        the moments to use as starting values for the fit
    :param values: The independent variable where the data is measured, optional
    :type values: Union[None, list]
    :param int num_points: Number of points to evaluate the data on, optional
    :param float int_thresh: Intensity threshold. If not None, only the rocking curves with
        higher ptp (range of values) are fitted, others are assumed to be noise and not important
        data. This parameter is used to accelerate the fit. Optional.

    :returns: If curve was fitted, the fitted curve, else item[0]
    :rtype: list
    """
    y, moments = y_values
    y = numpy.asanyarray(y)
    x = numpy.asanyarray(values) if values is not None else numpy.arange(len(y))
    if int_thresh is not None and y.ptp() < int_thresh:
        return y, [0, x[0], 0, min(y)]
    if moments is not None:
        p0 = [y.ptp(), moments[0], moments[1], min(y)]
    else:
        _sum = sum(y)
        if _sum > 0:
            mean = sum(x * y) / sum(y)
            sigma = numpy.sqrt(sum(y * (x - mean)**2) / sum(y))
        else:
            mean, sigma = 0, 0
        p0 = [y.ptp(), mean, sigma, min(y)]
    if numpy.isclose(p0[2], 0):
        return y, p0
    if num_points is None:
        num_points = len(y)
    try:
        pars, cov = curve_fit(f=gaussian, xdata=x, ydata=y, p0=p0, bounds=([min(y.ptp(), min(y)), min(x), -numpy.inf, -numpy.inf], [max(y), max(x), numpy.inf, numpy.inf]))
        y_gauss = gaussian(numpy.linspace(x[0], x[-1], num_points), *pars)
        y_gauss[numpy.isnan(y_gauss)] = 0
        y_gauss[y_gauss < 0] = 0
        return y_gauss, pars
    except RuntimeError:
        return y, p0


def fit_2d_rocking_curve(y_values, values, shape, int_thresh=None):

    y, moments = y_values
    y = numpy.asanyarray(y)
    A = y.ptp()
    values = numpy.asanyarray(values)
    _sum = sum(y)
    if numpy.isclose(_sum, 0, rtol=1e-03):
        return y, [numpy.nan, numpy.nan, numpy.nan, numpy.nan, A, 0, 0]
    x0 = sum(values[0] * y) / _sum
    y0 = sum(values[1] * y) / _sum
    xalpha = numpy.sqrt(sum(y * (values[0] - x0)**2) / _sum)
    yalpha = numpy.sqrt(sum(y * (values[1] - y0)**2) / _sum)
    if (int_thresh is not None and y.ptp() < int_thresh) or xalpha == 0 or yalpha == 0:
        return y, [x0, y0, xalpha, yalpha, A, 0, 0]
    X, Y = numpy.meshgrid(values[0, :shape[0]], values[1].reshape(numpy.flip(shape))[:, 0])
    xdata = numpy.vstack((X.ravel(), Y.ravel()))
    epsilon = 1e-3

    try:
        pars, cov = curve_fit(
            f=multi_gaussian,
            xdata=xdata,
            ydata=y,
            p0=[x0, y0, xalpha, yalpha, A, 0, 0],
            bounds=([
                    min(values[0]) - epsilon, min(values[1]) - epsilon, 0, 0, min(y.ptp(), min(y)), -1, -numpy.inf
                    ], [
                    max(values[0]) + epsilon, max(values[1]) + epsilon, numpy.inf, numpy.inf, max(y) + 1, 1, numpy.inf
                    ])
        )
        y_gauss = multi_gaussian([X, Y], *pars)
        return y_gauss.ravel(), pars
    except RuntimeError:
        return y, [x0, y0, xalpha, yalpha, A, 0, 0]


def fit_data(data, moments=None, values=None, shape=None, int_thresh=15, _tqdm=False):
    """
    Fit data in axis 0 of data

    :param bool _tqdm: If True, execut fitting under tqdm library.
    :returns: fitted data
    """

    g = generator(data, moments)
    cpus = multiprocessing.cpu_count()
    curves, maps = [], []
    with Pool(cpus - 1) as p:
        if _tqdm and tqdm is not None:
            for curve, pars in tqdm.tqdm(p.imap(partial(fit_rocking_curve, values=values, int_thresh=int_thresh), g), total=data.shape[1] * data.shape[2]):
                curves.append(list(curve))
                maps.append(list(pars))
        else:
            for curve, pars in p.map(partial(fit_rocking_curve, values=values, int_thresh=int_thresh), g):
                curves.append(list(curve))
                maps.append(list(pars))
    return numpy.array(curves).T.reshape(data.shape), numpy.array(maps).T.reshape((4, data.shape[-2], data.shape[-1]))


def fit_2d_data(data, values, shape, moments=None, int_thresh=15, _tqdm=False):
    """
    Fit data in axis 0 of data

    :param bool _tqdm: If True, execut fitting under tqdm library.
    :returns: fitted data
    """
    g = generator(data, moments)
    cpus = multiprocessing.cpu_count()
    curves, maps = [], []
    with Pool(cpus - 1) as p:
        if _tqdm and tqdm is not None:
            for curve, pars in tqdm.tqdm(p.imap(partial(fit_2d_rocking_curve, values=values, shape=shape, int_thresh=int_thresh), g), total=data.shape[-2] * data.shape[-1]):
                curves.append(list(curve))
                maps.append(list(pars))
        else:
            for curve, pars in p.map(partial(fit_2d_rocking_curve, values=values, shape=shape, int_thresh=int_thresh), g):
                curves.append(list(curve))
                maps.append(list(maps))
    return numpy.array(curves).T.reshape(data.shape), numpy.array(maps).T.reshape((7, data.shape[-2], data.shape[-1]))


def compute_moments(values, data):
    """
    Compute first, second, third and fourth moment of data on values.

    :returns: The four moments
    """
    stack = [values[i] * data[i] for i in range(len(data))]
    zsum = numpy.sum(data, axis=0)
    com = numpy.sum(stack, axis=0) / zsum
    com = medfilt2d(com.astype(numpy.float64))
    com[numpy.isnan(com)] = numpy.min(com[~numpy.isnan(com)])
    repeat_values = numpy.repeat(values, com.shape[0] * com.shape[1]).reshape(len(values), com.shape[0], com.shape[1])
    std = numpy.sqrt(sum((data[i] * ((repeat_values[i] - com)**2) for i in range(len(data))))) / zsum
    std = medfilt2d(std.astype(numpy.float64))
    std[numpy.isnan(std)] = numpy.min(std[~numpy.isnan(std)])
    skews = skew(stack, axis=0)
    kurt = kurtosis(stack, axis=0)

    return com, std, skews, kurt


def compute_peak_position(data, values=None, center_data=False):
    """
    Compute peak position map

    :param bool center_data: If True, the values are centered on 0.
    """
    if values is not None:
        values = numpy.asanyarray(values)
        x = numpy.array(numpy.argmax(data, axis=0))
        if center_data:
            middle = float(min(values) + values.ptp()) / 2
            values -= middle
        image = [values[i] for i in x.flatten()]
        image = numpy.reshape(image, x.shape)
    else:
        image = numpy.array(numpy.argmax(data, axis=0))
        if center_data:
            middle = len(data) / 2
            vals = numpy.linspace(-middle, middle, len(data))
            image = image * numpy.ptp(vals) / len(data) + numpy.min(vals)
    return image


def compute_rsm(H, W, d, ffz, mainx):
    """
    :param int H: height of the image in pixels.
    :param int W: width of the image in pixels.
    :param float d: Distance in micrometers of each pixel.
    :param float ffz: motor 'ffz' value.
    :param float mainx: motor 'mainx' value.

    :returns: Tuple of two arrays of size (W, H)
    :rtype: (X1, X2) : ndarray
    """
    pix_arr = numpy.meshgrid(numpy.arange(H), numpy.arange(W))
    pix_arr[0] = (pix_arr[0] - W / 2) * d
    pix_arr[1] = (H / 2 - pix_arr[1]) * d
    pix_arr[0] = numpy.degrees(numpy.arctan2(pix_arr[0], numpy.sqrt(ffz * ffz + mainx * mainx)))
    pix_arr[1] = numpy.degrees(numpy.arctan2(ffz - pix_arr[1], mainx))

    return pix_arr


def compute_magnification(H, W, d, obx, obpitch, mainx, topography=[False, 0], center=True):
    """
    :param int H: height of the image in pixels.
    :param int W: width of the image in pixels.
    :param float d: Distance in micrometers of each pixel.
    :param float obx: motor 'obx' value.
    :param float obpitch: motor 'obpitch' value in the middle of the dataset.
    :param float mainx: motor 'mainx' value.

    :returns: Tuple of two arrays of size (H, W)
    :rtype: (X1, X2) : ndarray
    """

    pix_arr = numpy.meshgrid(numpy.arange(H), numpy.arange(W))
    d1 = obx / numpy.cos(numpy.radians(obpitch))
    d2 = mainx / numpy.cos(numpy.radians(obpitch)) - d1
    M = d2 / d1
    d /= M
    if center:
        pix_arr[0] = (pix_arr[0] - W / 2) * d
        pix_arr[1] = (H / 2 - pix_arr[1]) * d
    else:
        pix_arr[0] = pix_arr[0] * d
        pix_arr[1] = (H - 1 - pix_arr[1]) * d
    if topography[0]:
        pix_arr[topography[1]] /= numpy.sin(numpy.radians(obpitch))
    return pix_arr
