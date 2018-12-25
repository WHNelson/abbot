from PyQt5 import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys








if __name__=='__main__':
    app = QtGui.QApplication([])
    win = pg.GraphicsWindow(title="Hello")
    win.resize(600,600)
    win.setWindowTitle('example: plotting')

    pg.setConfigOptions(antialias=True)

    p1 = win.addPlot(title="Basic array plot: ", y=np.random.normal(size=100))

    QtGui.QApplication.instance().exec_()
