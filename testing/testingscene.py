import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt)
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

class MainWindow(QtWidgets.QMainWindow):
    central_widget = None
    layout_container = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QWidget()
        self.layout_container = QVBoxLayout()
        self.central_widget.setLayout(self.layout_container)
        self.setCentralWidget(self.central_widget)
        self.layout_container.addWidget(GraphicsView())

class GraphicsView(QGraphicsView):

    start = None
    end = None
    item = None
    path = None

    def __init__(self):
        super(GraphicsView, self).__init__()
        self.setScene(QGraphicsScene())
        self.path = QtGui.QPainterPath()
        self.item = GraphicsPathItem()
        self.scene().addItem(self.item)

    def mousePressEvent(self, event):
        self.start = self.mapToScene(event.pos())
        self.path.moveTo(self.start)

    def mouseMoveEvent(self, event):
        self.end = self.mapToScene(event.pos())
        self.path.lineTo(self.end)
        self.start = self.end
        self.item.setPath(self.path)

class GraphicsPathItem(QtWidgets.QGraphicsPathItem):

    def __init__(self):
        super(GraphicsPathItem, self).__init__()
        pen = QtGui.QPen()
        pen.setColor(Qt.blue)
        pen.setWidth(3)
        self.setPen(pen)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())