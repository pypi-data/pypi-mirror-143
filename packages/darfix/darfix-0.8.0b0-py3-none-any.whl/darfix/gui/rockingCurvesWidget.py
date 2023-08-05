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
__date__ = "07/12/2021"

import numpy
import logging

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot import StackView, Plot2D
from silx.utils.enum import Enum as _Enum
from silx.io.dictdump import dicttonx
from silx.image.marchingsquares import find_contours

import darfix
from darfix.core.mapping import fit_rocking_curve, fit_2d_rocking_curve
from darfix.core.dataset import Operation
from .operationThread import OperationThread

_logger = logging.getLogger(__file__)


class Maps(_Enum):
    """
    Different maps that can be showed after fitting the data
    """
    AMPLITUDE = "Amplitude"
    FWHM = "FWHM"
    PEAK = "Peak position"
    BACKGROUND = "Background"
    RESIDUALS = "Residuals"


class Maps_2D(_Enum):
    """
    Different maps that can be showed after fitting the data
    """
    AMPLITUDE = "Amplitude"
    PEAK_X = "Peak position first motor"
    PEAK_Y = "Peak position second motor"
    FWHM_X = "FWHM first motor"
    FWHM_Y = "FWHM second motor"
    BACKGROUND = "Background"
    CORRELATION = "Correlation"
    RESIDUALS = "Residuals"


class RockingCurvesWidget(qt.QMainWindow):
    """
    Widget to apply fit to a set of images and plot the amplitude, fwhm, peak position, background and residuals maps.
    """
    sigFitted = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        widget = qt.QWidget(parent=self)
        layout = qt.QGridLayout()

        self._sv = StackView(parent=self, position=True)
        self._sv.setColormap(Colormap(name=darfix.config.DEFAULT_COLORMAP_NAME))
        self._plot = Plot2D(parent=self)
        self._plot.setDefaultColormap(Colormap(name='cividis', normalization='linear'))
        self._plot.setGraphTitle("Rocking curves")
        self._plot.setGraphXLabel("Degrees")
        intLabel = qt.QLabel("Intensity threshold:")
        self._intThresh = "15"
        self._intThreshLE = qt.QLineEdit(self._intThresh)
        self._intThreshLE.setValidator(qt.QDoubleValidator())
        self._computeFit = qt.QPushButton("Fit data")
        self._computeFit.clicked.connect(self._grainPlot)
        self._abortFit = qt.QPushButton("Abort")
        self._abortFit.clicked.connect(self.__abort)
        spacer1 = qt.QWidget(parent=self)
        spacer1.setLayout(qt.QVBoxLayout())
        spacer1.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._dimension = None
        self._motorValuesCheckbox = qt.QCheckBox("Use motor values")
        self._motorValuesCheckbox.setChecked(True)
        self._motorValuesCheckbox.stateChanged.connect(self._checkboxStateChanged)
        self._centerDataCheckbox = qt.QCheckBox("Center angle values")
        self._centerDataCheckbox.setEnabled(False)
        self._centerDataCheckbox.stateChanged.connect(self._checkboxStateChanged)
        self._parametersLabel = qt.QLabel("")
        self._plotMaps = Plot2D(self)
        self._plotMaps.setDefaultColormap(Colormap(name='cividis', normalization='linear'))
        self._plotMaps.hide()
        self._methodCB = qt.QComboBox(self)
        self._methodCB.hide()
        self._exportButton = qt.QPushButton("Export maps")
        self._exportButton.hide()
        self._exportButton.clicked.connect(self.exportMaps)

        layout.addWidget(self._sv, 0, 0, 1, 2)
        layout.addWidget(self._plot, 0, 2, 1, 2)
        layout.addWidget(self._parametersLabel, 1, 2, 1, 2)
        layout.addWidget(self._motorValuesCheckbox, 2, 2, 1, 1)
        layout.addWidget(self._centerDataCheckbox, 2, 3, 1, 1)
        layout.addWidget(intLabel, 3, 0, 1, 1)
        layout.addWidget(self._intThreshLE, 3, 1, 1, 1)
        layout.addWidget(self._computeFit, 3, 2, 1, 2)
        layout.addWidget(self._abortFit, 3, 2, 1, 2)
        layout.addWidget(self._methodCB, 4, 0, 1, 4)
        layout.addWidget(self._plotMaps, 5, 0, 1, 4)
        layout.addWidget(self._exportButton, 6, 0, 1, 5)
        self._abortFit.hide()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setDataset(self, parent, dataset, indices=None, bg_indices=None, bg_dataset=None):
        """
        Dataset setter.

        :param Dataset dataset: dataset
        """
        self._parent = parent
        self.dataset = dataset
        self.indices = indices
        self._update_dataset = dataset
        self.residuals = None
        self._thread = OperationThread(self, self.dataset.apply_fit)
        self.setStack()
        self._methodCB.clear()
        oldState = self._methodCB.blockSignals(True)
        if self.dataset.transformation:
            transformation = self.dataset.transformation.transformation
            px = transformation[0][0][0]
            py = transformation[1][0][0]
            xscale = (transformation[0][-1][-1] - px) / transformation[0].shape[1]
            yscale = (transformation[1][-1][-1] - py) / transformation[1].shape[0]
            self.origin = (px, py)
            self.scale = (xscale, yscale)
        else:
            self.origin, self.scale = None, None
        if self.dataset.dims.ndim == 2:
            self._methodCB.addItems(Maps_2D.values())
            self._methodCB.currentTextChanged.connect(self._update2DPlot)
        else:
            self._methodCB.addItems(Maps.values())
            self._methodCB.currentTextChanged.connect(self._updatePlot)
        self._methodCB.blockSignals(oldState)
        self._sv.getPlotWidget().sigPlotSignal.connect(self._mouseSignal)
        self._sv.sigFrameChanged.connect(self._addPoint)

    def setStack(self, dataset=None):
        """
        Sets new data to the stack.
        Mantains the current frame showed in the view.

        :param Dataset dataset: if not None, data set to the stack will be from the given dataset.
        """
        if dataset is None:
            dataset = self.dataset
        nframe = self._sv.getFrameNumber()
        if self.indices is None:
            self._sv.setStack(dataset.get_data() if dataset is not None else None)
        else:
            self._sv.setStack(dataset.get_data(self.indices) if dataset is not None else None)
        self._sv.setFrameNumber(nframe)

    def getStackViewColormap(self):
        """
        Returns the colormap from the stackView

        :rtype: silx.gui.colors.Colormap
        """
        return self._sv.getColormap()

    def setStackViewColormap(self, colormap):
        """
        Sets the stackView colormap

        :param colormap: Colormap to set
        :type colormap: silx.gui.colors.Colormap
        """
        self._sv.setColormap(colormap)

    def _mouseSignal(self, info):
        """
        Method called when a signal from the stack is called
        """
        if info['event'] == 'mouseClicked':
            # In case the user has clicked on a pixel in the stack
            data = self.dataset.get_data(self.indices)
            px = info['x']
            py = info['y']
            # Show vertical and horizontal lines for clicked pixel
            self._sv.getPlotWidget().addCurve((px, px), (0, data.shape[1]), legend='x', color='r')
            self._sv.getPlotWidget().addCurve((0, data.shape[2]), (py, py), legend='y', color='r')
            self.plotRockingCurves(data, px, py)

    def _addPoint(self, i):
        """
        Slot to add curve for frame number in rocking curves plot.

        :param int i: frame number
        """
        try:
            if len(self.y.shape) == 2:
                xdim = self.dataset.dims.get(1)
                ydim = self.dataset.dims.get(0)
                dotx = int(i / ydim.size)
                doty = i % ydim.size
                if self._motorValuesCheckbox.isChecked():
                    dotx = xdim.unique_values[dotx]
                    doty = ydim.unique_values[doty]
                else:
                    xscale = xdim.range[2]
                    yscale = ydim.range[2]
                    if self._centerDataCheckbox.isChecked():
                        dotx -= xdim.size // 2
                        doty -= ydim.size // 2
                    dotx *= xscale
                    doty *= yscale
                self._plot.addCurve(
                    [dotx], [doty], symbol='o', legend='dot_o', color='b'
                )
            else:
                self._plot.clear()
                self._plot.addCurve(
                    [self.x[i]], [self.y[i]], symbol='o', legend='dot_o',
                    color='b'
                )
                i_gauss = i * int((len(self.y_gauss) - 1) / (len(self.x) - 1))
                self._plot.addCurve(
                    [self.x_gauss[i_gauss]], [self.y_gauss[i_gauss]], symbol='o',
                    legend='dot_fit', color='r'
                )
        # TODO
        except (ValueError, TypeError, AttributeError):
            pass

    def _computeContours(self, image, origin=None, scale=None):
        polygons = []
        levels = []
        for i in numpy.linspace(numpy.min(image), numpy.max(image), 10):
            polygons.append(find_contours(image, i))
            levels.append(i)
        # xdim = self.dataset.dims.get(1)
        # ydim = self.dataset.dims.get(0)
        for ipolygon, polygon in enumerate(polygons):
            # iso contours
            for icontour, contour in enumerate(polygon):
                if len(contour) == 0:
                    continue
                # isClosed = numpy.allclose(contour[0], contour[-1])
                x = contour[:, 1]
                y = contour[:, 0]
                if scale is not None:
                    x *= scale[0]
                    y *= scale[1]
                    x += origin[0] + scale[0] / 2
                    y += origin[1] + scale[1] / 2
                legend = "poly{}.{}".format(icontour, ipolygon)
                self._plot.addCurve(x=x, y=y, linestyle="-", linewidth=2.0,
                                    legend=legend, resetzoom=False, color='w')

    def plotRockingCurves(self, data, px, py):
        """
        Plot rocking curves of data and fitted data at pixel (px, py).

        :param Data data: stack of images to plot
        :param px: x pixel
        :param py: y pixel
        """
        # Get rocking curves from data
        self._plot.clear()
        try:
            if self.dataset.in_memory:
                y = data[:, int(py), int(px)]
            else:
                y = numpy.array([image[int(py), int(px)] for image in data])
        except IndexError:
            _logger.warning("Index out of bounds")
            return
        if self.dataset.dims.ndim == 2:
            xdim = self.dataset.dims.get(1)
            ydim = self.dataset.dims.get(0)
            self._plot.remove(kind='curve')
            frameNumber = self._sv.getFrameNumber()
            x = [
                self.dataset.get_metadata_values(kind=ydim.kind, key=ydim.name),
                self.dataset.get_metadata_values(kind=xdim.kind, key=xdim.name)
            ]
            dotx = int(frameNumber / ydim.size)
            doty = frameNumber % ydim.size
            xscale = xdim.range[2]
            yscale = ydim.range[2]
            if self._motorValuesCheckbox.isChecked():
                origin = [xdim.range[0], ydim.range[0]]
                dotx = xdim.unique_values[dotx]
                doty = ydim.unique_values[doty]
            else:
                origin = (0., 0.)
                if self._centerDataCheckbox.isChecked():
                    dotx -= int(xdim.size / 2)
                    doty -= int(ydim.size / 2)
                    origin = (- xscale * int(xdim.size / 2), - yscale * int(ydim.size / 2))
                dotx *= xscale
                doty *= yscale
            try:
                y_gauss, pars = fit_2d_rocking_curve([y, None], values=x, shape=[ydim.size, xdim.size])
                if numpy.array_equal(y_gauss, y):
                    raise RuntimeError
                y_gauss = numpy.reshape(y_gauss, (ydim.size, xdim.size))
                self._computeContours(y_gauss, origin, (xscale, yscale))
                self._parametersLabel.setText("PEAK_X:{:.3f} PEAK_Y:{:.3f} FWHM_X:{:.3f} FWHM_Y:{:.3f} AMP:{:.3f} CORR:{:.3f} BG:{:.3f}".format(*pars))
            except (TypeError, RuntimeError):
                y_gauss = y
                _logger.warning("Cannot fit")

            y = numpy.reshape(y, (ydim.size, xdim.size))
            self._plot.addImage(y, xlabel=xdim.name, ylabel=ydim.name, origin=origin, scale=(xscale, yscale))
            self._plot.addCurve([dotx], [doty], symbol='o', legend='dot_o', color='b')
            self.x, self.x_gauss, self.y, self.y_gauss = x, x, y, y_gauss
        else:
            if self.dataset.dims.ndim == 0:
                x = numpy.arange(data.shape[0])
            else:
                dim = self.dataset.dims.get(0)
                if self._motorValuesCheckbox.isChecked():
                    x = numpy.array(self.dataset.get_metadata_values(
                        kind=dim.kind, key=dim.name, indices=self.indices))
                else:
                    scale = dim.range[2]
                    x = numpy.arange(data.shape[0]) * scale
                    if self._centerDataCheckbox.isChecked():
                        x -= int(dim.size / 2)

            item = [numpy.array(y), None]
            if self._centerDataCheckbox.isChecked():
                middle = (float(x[-1]) - float(x[0])) / 2
                # x = numpy.linspace(-middle, middle, len(x))
                x -= float(x[0]) + middle
            # Show rocking curves and fitted curve into plot
            self._plot.clear()
            self._plot.addCurve(x, y, legend="data", color='b')
            i = self._sv.getFrameNumber()
            try:
                y_gauss, pars = fit_rocking_curve(item, values=x, num_points=1000)
                self._parametersLabel.setText("PEAK:{:.3f} FWHM:{:.3f} AMP:{:.3f} BG:{:.3f}".format(*pars))
            except TypeError:
                y_gauss = y
                _logger.warning("Cannot fit")

            # Add curves (points) for stackview frame number
            self.x_gauss = numpy.linspace(x[0], x[-1], len(y_gauss))
            self._plot.addCurve(self.x_gauss, y_gauss, legend="fit", color='r')
            self._plot.addCurve([x[i]], [y[i]], symbol='o', legend='dot_o', color='b')
            i_gauss = i * int((len(y_gauss) - 1) / (len(x) - 1))
            self._plot.addCurve([self.x_gauss[i_gauss]], [y_gauss[i_gauss]], symbol='o', legend='dot_fit', color='r')
            self.x, self.y, self.y_gauss = x, y, y_gauss

    def _grainPlot(self):
        """
        Method called when button for computing fit is clicked
        """
        self._computeFit.hide()
        self._intThresh = self._intThreshLE.text()
        self.sigFitted.emit()
        self._thread.setArgs(self.indices, self._dimension, float(self._intThresh))
        self._thread.finished.connect(self._updateData)
        self._thread.start()
        self._abortFit.show()

    def _updatePlot(self, method):
        """
        Updates the plots with the chosen method
        """
        try:
            method = Maps(method)
            label = self.dataset.transformation.label if self.dataset.transformation is not None else "pixels"
            if method == Maps.AMPLITUDE:
                self._plotMaps.addImage(self.maps[0], origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps.FWHM:
                std = self.maps[2]
                std[numpy.isnan(std)] = 0
                self._plotMaps.addImage(darfix.config.FWHM_VAL * std, origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps.PEAK:
                com = self.maps[1]
                com[numpy.isnan(com)] = min(com[~numpy.isnan(com)])
                self._plotMaps.addImage(com, origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps.BACKGROUND:
                self._plotMaps.addImage(self.maps[3], origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps.RESIDUALS:
                self._plotMaps.addImage(numpy.sqrt(numpy.subtract(
                    self._update_dataset.zsum(self.indices), self.dataset.zsum(self.indices)) ** 2),
                    origin=self.origin, scale=self.scale, xlabel=label, ylabel=label)
        except ValueError:
            _logger.warning("Unexisting map method")

    def _update2DPlot(self, method):
        """
        Updates the plots with the chosen method
        """
        try:
            method = Maps_2D(method)
            label = self.dataset.transformation.label if self.dataset.transformation is not None else "pixels"
            if method == Maps_2D.PEAK_X:
                com = self.maps[0]
                com[numpy.isnan(com)] = min(com[~numpy.isnan(com)])
                self._plotMaps.addImage(com, origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps_2D.PEAK_Y:
                com = self.maps[1]
                com[numpy.isnan(com)] = min(com[~numpy.isnan(com)])
                self._plotMaps.addImage(com, origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps_2D.FWHM_X:
                std = self.maps[2]
                std[numpy.isnan(std)] = 0
                self._plotMaps.addImage(darfix.config.FWHM_VAL * std, origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps_2D.FWHM_Y:
                std = self.maps[3]
                std[numpy.isnan(std)] = 0
                self._plotMaps.addImage(darfix.config.FWHM_VAL * std, origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps_2D.AMPLITUDE:
                self._plotMaps.addImage(self.maps[4], origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps_2D.CORRELATION:
                self._plotMaps.addImage(self.maps[5], origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps_2D.BACKGROUND:
                self._plotMaps.addImage(self.maps[6], origin=self.origin, scale=self.scale,
                                        xlabel=label, ylabel=label)
            elif method == Maps_2D.RESIDUALS:
                self._plotMaps.addImage(numpy.sqrt(numpy.subtract(
                    self._update_dataset.zsum(self.indices), self.dataset.zsum(self.indices)) ** 2),
                    origin=self.origin, scale=self.scale, xlabel=label, ylabel=label)
        except ValueError:
            _logger.warning("Unexisting map method")

    def __abort(self):
        self._abortFit.setEnabled(False)
        self.dataset.stop_operation(Operation.FIT)

    def _updateData(self):
        """
        Method called when fit computation has finished
        """
        self._thread.finished.disconnect(self._updateData)
        self._abortFit.hide()
        self._computeFit.show()
        if self._thread.data:
            self._update_dataset, self.maps = self._thread.data
            assert self._update_dataset is not None
            self.residuals = numpy.sqrt(numpy.subtract(
                self._update_dataset.zsum(self.indices), self.dataset.zsum(self.indices)) ** 2)
            if self.dataset.dims.ndim == 2:
                self._update2DPlot(self._methodCB.currentText())
            else:
                self._updatePlot(self._methodCB.currentText())
            self._plotMaps.show()
            self._methodCB.show()
            self._exportButton.show()
        else:
            print("\nCorrection aborted")

    def _wholeStack(self):
        self._dimension = None
        self.setStack(self.dataset)
        xc = self._sv.getPlotWidget().getCurve('x')
        if xc:
            px = xc.getXData()[0]
            py = self._sv.getPlotWidget().getCurve('y').getYData()[0]
            self.plotRockingCurves(self.dataset.get_data(self.indices), px, py)

    def _checkboxStateChanged(self):
        """
        Update widgets linked to the checkbox state
        """
        self._centerDataCheckbox.setEnabled(not self._motorValuesCheckbox.isChecked())
        data = self.dataset.get_data(self.indices, self._dimension)
        xc = self._sv.getPlotWidget().getCurve('x')
        if xc:
            px = xc.getXData()[0]
            py = self._sv.getPlotWidget().getCurve('y').getYData()[0]
            self.plotRockingCurves(data, px, py)
        if Maps(self._methodCB.currentText()) == Maps.PEAK:
            self._updatePlot(Maps.PEAK)

    @property
    def intThresh(self):
        return self._intThresh

    @intThresh.setter
    def intThresh(self, intThresh):
        self._intThresh = intThresh
        self._intThreshLE.setText(intThresh)

    @property
    def dimension(self):
        return self._dimension

    def exportMaps(self):
        """
        Creates dictionay with maps information and exports it to a nexus file
        """
        entry = "entry"

        if self.dataset.dims.ndim == 2:
            std_x = self.maps[2]
            std_x[numpy.isnan(std_x)] = 0
            std_y = self.maps[3]
            std_y[numpy.isnan(std_y)] = 0
            maps = {
                Maps_2D.PEAK_X.name: self.maps[0],
                Maps_2D.PEAK_Y.name: self.maps[1],
                Maps_2D.FWHM_X.name: darfix.config.FWHM_VAL * std_x,
                Maps_2D.FWHM_Y.name: darfix.config.FWHM_VAL * std_y,
                Maps_2D.AMPLITUDE.name: self.maps[4],
                Maps_2D.CORRELATION.name: self.maps[5],
                Maps_2D.BACKGROUND.name: self.maps[6],
                Maps_2D.RESIDUALS.name: self.residuals,
                "@NX_class": "NXcollection"
            }
        else:
            std = self.maps[2]
            std[numpy.isnan(std)] = 0
            maps = {
                Maps.AMPLITUDE.name: self.maps[0],
                Maps.FWHM.name: darfix.config.FWHM_VAL * std,
                Maps.PEAK.name: self.maps[1],
                Maps.RESIDUALS.name: self.residuals,
                "@NX_class": "NXcollection"
            }

        nx = {
            entry: {
                "data": {
                    ">" + Maps.AMPLITUDE.name: "../maps/" + Maps.AMPLITUDE.name,
                    "@signal": Maps.AMPLITUDE.name,
                    "@NX_class": "NXdata"
                },
                "maps": maps,
                "@NX_class": "NXentry",
                "@default": "data",
            },
            "@NX_class": "NXroot",
            "@default": "entry"
        }

        fileDialog = qt.QFileDialog()

        fileDialog.setFileMode(fileDialog.AnyFile)
        fileDialog.setAcceptMode(fileDialog.AcceptSave)
        fileDialog.setOption(fileDialog.DontUseNativeDialog)
        fileDialog.setDefaultSuffix(".h5")
        if fileDialog.exec_():
            dicttonx(nx, fileDialog.selectedFiles()[0])
