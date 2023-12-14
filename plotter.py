import sys

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np
from rplidar import RPLidar


def dict_to_x_y(dict):
    angles = np.deg2rad(np.array(list(dict.keys())))
    distances = np.array(list(dict.values()))
    x = distances * np.sin(angles)
    y = distances * np.cos(angles)
    return x, y


class LidarPlotter(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LidarPlotter, self).__init__(parent)
        self.lidar = RPLidar('COM9', baudrate=256000)
        self.room = {}
        self.persons = {}

        self.initUI()

    def initUI(self):
        self.graphWidget = pg.PlotWidget()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.graphWidget)
        self.setLayout(self.layout)

        self.graphWidget.setYRange(-5000, 5000)
        self.graphWidget.setXRange(-5000, 5000)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Adjust the time interval for updates

    def _draw_room(self):
        scan = next(self.lidar.iter_scans())
        angles = np.deg2rad(np.array([item[1] for item in scan]))
        distances = np.array([item[2] for item in scan])
        x = distances * np.cos(angles)
        y = distances * np.sin(angles)
        # x, y = dict_to_x_y(self.room)
        self.graphWidget.plot(x, y, pen=None, symbol='o', color=(255, 255, 255))

    def _draw_persons(self):
        x, y = dict_to_x_y(self.persons)
        self.graphWidget.plot(x, y, pen=None, symbol='o', color=(255, 255, 255))

    def update(self):

        self.graphWidget.clear()
        self._draw_room()
        # self._draw_persons()

    def set_room(self, room):
        self.room = room
        # self.update()

    def set_persons(self, persons):
        self.persons = persons
        # self.update()

app = QtWidgets.QApplication(sys.argv)
ex = LidarPlotter()
ex.show()
sys.exit(app.exec_())
