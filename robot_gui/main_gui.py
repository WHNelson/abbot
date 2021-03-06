# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pi/projects/robot_reboot/robot_gui/main_gui.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_gui(object):
    def setupUi(self, main_gui):
        main_gui.setObjectName("main_gui")
        main_gui.resize(604, 515)
        self.centralWidget = QtWidgets.QWidget(main_gui)
        self.centralWidget.setObjectName("centralWidget")
        self.btnClosePort = QtWidgets.QPushButton(self.centralWidget)
        self.btnClosePort.setGeometry(QtCore.QRect(120, 220, 81, 31))
        self.btnClosePort.setObjectName("btnClosePort")
        self.btnStartReader = QtWidgets.QPushButton(self.centralWidget)
        self.btnStartReader.setGeometry(QtCore.QRect(10, 220, 91, 31))
        self.btnStartReader.setObjectName("btnStartReader")
        self.sldServoVal = QtWidgets.QSlider(self.centralWidget)
        self.sldServoVal.setGeometry(QtCore.QRect(10, 190, 191, 20))
        self.sldServoVal.setMaximum(180)
        self.sldServoVal.setSliderPosition(90)
        self.sldServoVal.setOrientation(QtCore.Qt.Horizontal)
        self.sldServoVal.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.sldServoVal.setTickInterval(10)
        self.sldServoVal.setObjectName("sldServoVal")
        self.btnAutoRange = QtWidgets.QPushButton(self.centralWidget)
        self.btnAutoRange.setGeometry(QtCore.QRect(290, 380, 84, 25))
        self.btnAutoRange.setObjectName("btnAutoRange")
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setGeometry(QtCore.QRect(270, 20, 16, 391))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 261, 171))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblComStatus = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lblComStatus.setObjectName("lblComStatus")
        self.verticalLayout.addWidget(self.lblComStatus)
        self.lblDistance = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lblDistance.setObjectName("lblDistance")
        self.verticalLayout.addWidget(self.lblDistance)
        self.lblServo = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lblServo.setObjectName("lblServo")
        self.verticalLayout.addWidget(self.lblServo)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lneSendVal = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lneSendVal.setObjectName("lneSendVal")
        self.verticalLayout.addWidget(self.lneSendVal)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblComStatusVal = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lblComStatusVal.setObjectName("lblComStatusVal")
        self.verticalLayout_2.addWidget(self.lblComStatusVal)
        self.lblDistanceVal = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lblDistanceVal.setObjectName("lblDistanceVal")
        self.verticalLayout_2.addWidget(self.lblDistanceVal)
        self.lblServoVal = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lblServoVal.setObjectName("lblServoVal")
        self.verticalLayout_2.addWidget(self.lblServoVal)
        self.lblServoVal_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lblServoVal_2.setObjectName("lblServoVal_2")
        self.verticalLayout_2.addWidget(self.lblServoVal_2)
        self.btnSend = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnSend.setObjectName("btnSend")
        self.verticalLayout_2.addWidget(self.btnSend)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gvwJoystick = QtWidgets.QGraphicsView(self.centralWidget)
        self.gvwJoystick.setGeometry(QtCore.QRect(290, 180, 256, 192))
        self.gvwJoystick.setObjectName("gvwJoystick")
        self.btnForward = QtWidgets.QPushButton(self.centralWidget)
        self.btnForward.setGeometry(QtCore.QRect(440, 20, 31, 25))
        self.btnForward.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/up2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnForward.setIcon(icon)
        self.btnForward.setObjectName("btnForward")
        self.btnBack = QtWidgets.QPushButton(self.centralWidget)
        self.btnBack.setGeometry(QtCore.QRect(440, 60, 31, 25))
        self.btnBack.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../images/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnBack.setIcon(icon1)
        self.btnBack.setObjectName("btnBack")
        self.btnRight = QtWidgets.QPushButton(self.centralWidget)
        self.btnRight.setGeometry(QtCore.QRect(480, 40, 31, 25))
        self.btnRight.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../images/right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRight.setIcon(icon2)
        self.btnRight.setObjectName("btnRight")
        self.btnLeft = QtWidgets.QPushButton(self.centralWidget)
        self.btnLeft.setGeometry(QtCore.QRect(400, 40, 31, 25))
        self.btnLeft.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../images/left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLeft.setIcon(icon3)
        self.btnLeft.setObjectName("btnLeft")
        main_gui.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(main_gui)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 604, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        main_gui.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(main_gui)
        self.mainToolBar.setObjectName("mainToolBar")
        main_gui.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(main_gui)
        self.statusBar.setObjectName("statusBar")
        main_gui.setStatusBar(self.statusBar)
        self.actionExit = QtWidgets.QAction(main_gui)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(main_gui)
        self.actionExit.triggered.connect(main_gui.close)
        QtCore.QMetaObject.connectSlotsByName(main_gui)

    def retranslateUi(self, main_gui):
        _translate = QtCore.QCoreApplication.translate
        main_gui.setWindowTitle(_translate("main_gui", "main_gui"))
        self.btnClosePort.setText(_translate("main_gui", "Close Port"))
        self.btnStartReader.setText(_translate("main_gui", "Start Reader"))
        self.btnAutoRange.setText(_translate("main_gui", "Auto range"))
        self.lblComStatus.setText(_translate("main_gui", "K-Value returned:"))
        self.lblDistance.setText(_translate("main_gui", "Distance:"))
        self.lblServo.setText(_translate("main_gui", "Servo angle ret:"))
        self.label.setText(_translate("main_gui", "Set Value (k-value):"))
        self.lneSendVal.setInputMask(_translate("main_gui", "####"))
        self.lneSendVal.setText(_translate("main_gui", "1000"))
        self.lblComStatusVal.setText(_translate("main_gui", "_value_"))
        self.lblDistanceVal.setText(_translate("main_gui", "_value_"))
        self.lblServoVal.setText(_translate("main_gui", "_value_"))
        self.lblServoVal_2.setText(_translate("main_gui", "_value_"))
        self.btnSend.setText(_translate("main_gui", "Send"))
        self.menuFile.setTitle(_translate("main_gui", "File"))
        self.actionExit.setText(_translate("main_gui", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_gui = QtWidgets.QMainWindow()
    ui = Ui_main_gui()
    ui.setupUi(main_gui)
    main_gui.show()
    sys.exit(app.exec_())

