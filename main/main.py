#--------------------------------------------------------------------------------
#req'd imports

import sys
# print(sys.path)
# sys.path.insert(0, "../")
# print(sys.path)

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QDir, QSettings, QRect, QCoreApplication
from main_gui import main_gui
from myserial import stream

#define some constants
ORGANIZATION_NAME = 'Project Nebulous'
ORGANIZATION_DOMAIN = '/projectcebulous.com'
APPLICATION_NAME = 'test'
MAIN_GEOMETRY = 'settings/main_geometry'
SETTINGS_FILENAME = '/settings.conf'
DEFAULT_SIZE = QRect(950,500,300,350)
#--------------------------------------------------------------------------------



class RobotMain(QMainWindow, main_gui.Ui_main_gui):
    def __init__(self, parent=None):
        super(RobotMain, self).__init__(parent)
        self.setupUi(self)

        #setup a settings file and use the settings to set the geometry... uses QSettings, QDir, and QRect
        self.settings = QSettings(QDir().absolutePath() + ORGANIZATION_DOMAIN + SETTINGS_FILENAME,0,self)
        self.setGeometry(self.settings.value(MAIN_GEOMETRY, DEFAULT_SIZE)) #load geometry from file ... load(key, default)

        #create a manager
        self.boss = stream.RSerial()
     
        # Connect up signals
        self.boss.data_ready.connect(self.onDataReady) #connect the manager events to local functions
        
        #connect up the form buttons to RSerail slots
        self.btnClosePort.clicked.connect(self.boss.rclose)
        self.btnStartReader.clicked.connect(self.boss.ropen)
        self.btnSend.clicked.connect(self.senddata)
        self.sldServoVal.valueChanged.connect(self.sliderchanged)
    
        #setup some variables
        self.i = 0
       
    def save_settings(self):
        #save settings on exit
        self.boss.rclose()
        self.settings.setValue(MAIN_GEOMETRY, self.geometry()) #save geometry to file ... save(key, value)
        self.settings.sync()

    def senddata(self):
        #TODO: give the line edits some sort of ID to send along to the arduino
        id = 1
        if (self.lneSendVal.text() != ""):
            self.boss.rwrite([id,self.lneSendVal.text()])

    def sliderchanged(self, val):
        id = 2
        self.boss.rwrite([id,self.sldServoVal.value()])
        #print([id, self.sldServoVal.value()])

    def onDataReady(self, val):
        #TODO: define a return index for the data, for now we are caling 1
        index = 1
        self.lblDistanceVal.setText(str(val[index]))
        self.lblComStatusVal.setText(str(val[2]))

    
#--------------------------------------------
#run the program...if it's run as main
#--------------------------------------------
if __name__ == '__main__':

    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = QApplication(sys.argv)
    gui = RobotMain()
    gui.show()
    app.aboutToQuit.connect(gui.save_settings)
    app.exec_() 