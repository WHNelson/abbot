#--------------------------------------------------------------------------------
#req'd imports
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QDir, QSettings, QRect, QCoreApplication
from robot_gui import main_gui
from myserial import stream
import sys

#define some constants
RX_PACKET_FORMAT = '<BBBBBBHHH'     #hardcode the receive packet format
SERIAL_PORT = '/dev/ttyACM0'        #hardcode the com port for now
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
        self.boss = stream.Manager()
        # self.boss.managerInc.connect(self.onManagerInc) #connect the manager events to local functions
     
        # Connect up signals
        self.boss.dataReady.connect(self.onDataReady) #connect the manager events to local functions
        self.boss.comStatus.connect(self.onComStatus)

        # #connect up the form buttons to manager slots
        self.btnClosePort.clicked.connect(self.btnClosePortClick)
        self.btnStartReader.clicked.connect(self.boss.restartCom)
        self.btnSend.clicked.connect(self.senddata)
        # self.btnStopReader.clicked.connect(self.boss.close)
        # #self.btnPauseReader.clicked.connect(self.boss.pauseReader)
    


        #setup some variables
        self.i = 0
        #wierd timing issue ... this works here but ont in the worker init.
        self.lblComStatusVal.setText("open") if self.boss.ser.is_open else self.lblComStatusVal.setText("closed")

    def btnClosePortClick(self):
            self.boss.close()


    #save settings on exit
    #@pyqtSlot()
    def save_settings(self):
        self.settings.setValue(MAIN_GEOMETRY, self.geometry()) #save geometry to file ... save(key, value)
        self.settings.sync()


    #@pyqtSlot()
    def senddata(self):
        if (self.lneSendVal.text() != ""):
            self.boss.send(self.lneSendVal.text())

    #@pyqtSlot()
    def inc(self):
        self.i+=1
        print("i: ", self.i)
        self.lblDistanceVal.setText(str(self.i))
        return(self.i)

    #@pyqtSlot()
    def onManagerInc(self, val):
        #self.lblDistanceVal.setText(str(val))
        print(val)

    #@pyqtSlot()
    def onDataReady(self, val):
        self.lblDistanceVal.setText(str(val[0]))

    #@pyqtSlot()
    def onComStatus(self, val):
        self.lblComStatusVal.setText(val)
        print("setting lblcomstatusval to", val)
        self.lblComStatusVal.setText("open") if self.boss.ser.is_open else self.lblComStatusVal.setText("closed")


    
    


    
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