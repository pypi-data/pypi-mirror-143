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
__date__ = "09/12/2021"


from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot.StackView import StackViewMainWindow

import darfix
from .operationThread import OperationThread


class ProjectionWidget(qt.QMainWindow):
    """
    Widget to apply a projection to the chosen dimension.
    """
    sigComputed = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self._dimension = None

        self._sv = StackViewMainWindow()
        self._sv.setColormap(Colormap(name=darfix.config.DEFAULT_COLORMAP_NAME,
                                      normalization="linear"))
        dimensionLabel = qt.QLabel("Dimension:")
        self._dimensionCB = qt.QComboBox()
        self._projectButton = qt.QPushButton("Project data")
        self._projectButton.setEnabled(False)
        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self._buttons.setEnabled(False)
        layout = qt.QGridLayout()
        layout.addWidget(dimensionLabel, 0, 0)
        layout.addWidget(self._dimensionCB, 0, 1)
        layout.addWidget(self._projectButton, 1, 1)
        layout.addWidget(self._sv, 2, 0, 1, 2)
        layout.addWidget(self._buttons, 3, 1)
        self._sv.hide()
        widget = qt.QWidget()
        widget.setLayout(layout)

        self._buttons.accepted.connect(self.sigComputed.emit)
        self._projectButton.clicked.connect(self._projectData)

        self.setCentralWidget(widget)

    def setDataset(self, parent, dataset, indices=None, bg_indices=None, bg_dataset=None):
        """
        Dataset setter.

        :param Dataset dataset: dataset
        """

        if dataset is not None:
            self._parent = parent
            self._dataset = dataset
            self._update_dataset = dataset
            self.indices = indices
            self.bg_indices = bg_indices
            self.bg_dataset = bg_dataset
            self._projectButton.setEnabled(True)
            self._buttons.setEnabled(True)
            self._dimensionCB.clear()

            for dimension in self._dataset.dims:
                self._dimensionCB.insertItem(dimension[0], dimension[1].name)
            self._thread = OperationThread(self, self._dataset.project_data)

    def getDataset(self, update=None):
        return self._update_dataset, self.indices, self.bg_indices, self.bg_dataset

    def clearStack(self):
        self._sv.setStack(None)
        self._projectButton.setEnabled(False)

    @property
    def dimension(self):
        return self._dimension

    @dimension.setter
    def dimension(self, dimension):
        self._dimension = dimension

    def _projectData(self):
        self._projectButton.setEnabled(False)
        self.dimension = self._dimensionCB.currentIndex()
        self._thread.setArgs(dimension=self.dimension, indices=self.indices)
        self._thread.finished.connect(self._updateData)
        self._thread.start()

    def _updateDataset(self, widget, dataset):
        self._parent._updateDataset(widget, dataset)
        self._dataset = dataset

    def _updateData(self):
        self._projectButton.setEnabled(True)
        self._thread.finished.disconnect(self._updateData)
        if self._thread.data:
            del self._update_dataset
            self._update_dataset = self._thread.data
            self._sv.show()
            self._sv.setGraphTitle("Projection to dimension " + self._dataset.dims.get(self.dimension).name)
            self._sv.setStack(self._update_dataset.get_data())
