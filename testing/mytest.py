import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QGraphicsScene, QWidget, QApplication, QVBoxLayout,
                             QGraphicsPathItem, QMainWindow, QGraphicsView)
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt
from PyQt5.QtGui import QPainterPath, QPen


class main(QMainWindow):
    central_widget = None
    layout = None

    def __init__(self):
        super(main, self).__init__()
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.layout.addWidget(gview())

class gview(QGraphicsView):
    start = None
    end = None
    item = None
    path = None

    def __init__(self):
        super(gview, self).__init__()
        self.setScene(QGraphicsScene())
        self.path = QPainterPath()
        self.item = pathItem()
        self.scene().addItem(self.item)
        print("gview init")

    def mousePressEvent(self, event):
        self.start = self.mapToScene(event.pos())
        self.path.moveTo(self.start)
        print("mouse press")

    def mouseMoveEvent(self, event):
        self.end = self.mapToScene(event.pos())
        self.path.lineTo(self.end)
        self.start = self.end
        self.item.setPath(self.path)
        print("mouse move: ", event.pos())

class pathItem(QGraphicsPathItem):
    def __init__(self):
        super(pathItem, self).__init__()
        pen = QPen()
        pen.setColor(Qt.blue)
        pen.setWidth(2)
        self.setPen(pen)

if __name__=='__main__':
    app = QApplication(sys.argv)
    main_window = main()
    main_window.show()
    sys.exit(app.exec_())
