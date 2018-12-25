
#region - imports and aliases --------------------------------
# Put some header information here
#------------------------------------------------
# imports
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread, QEvent
import sys
import time
import struct
import serial
from cobs import cobs
import binascii
import crc16
import queue




#define some constants
PACKET_START = b'STRT'
PACKET_STOP = b'\x0A'
PACKET_LEN = 6 #total len has a header added to it... so PACKET_LEN+(1 - 4) for header
RXPACKET_FORMAT = "4H"
TXPACKET_FORMAT = "3H"
SERIAL_PORT = '/dev/ttyACM0'

#endregion - imports and aliases --------------------------------

#region - Manager Object ---------------------------------
class Manager(QObject):
    managerInc = pyqtSignal(int)
    dataReady = pyqtSignal(tuple)
    comStatus = pyqtSignal(str)


    def __init__(self):
        super().__init__()

        self.i = 0
        self.q = queue.Queue()

        self.ser = self.openPort() #TODO: don't really need self here.. I don't think

        self.events = MyEvents() #creates a MyEvents() object to hold event flags
        self.worker = Worker(self.events, self.ser, self.q) #make a worker passing it the event flags, serial object, and a reference to the queue
        self.worker.dataReady.connect(self.dataReady) #forward up the signal
        self.worker.comStatus.connect(self.comStatus) #forward up the signal

        self.worker_thread = QThread() #create a thread
        self.worker.moveToThread(self.worker_thread) #move the worker to the thread

        self.worker.finished.connect(self.worker_thread.quit) #tie the finished signal to the thread quit slot
        self.worker_thread.started.connect(self.worker.run) #tie the thread start to the read loop

        self.worker_thread.start() #start the thread

        self.txdata = 0 #declare a class level variable to hold the txdata

#endregion - Manager Object ---------------------------------

#region---create slots --------------------------
# Create slots
# inc() - to increment and return some test data
# setPort() - future - to be able to write to the settings file
# openPort() - opens the serial port - future: read from settings file
# close() - stop loop
# read() - set loop to reading mode
# write() - next step - set loop towriting mode
#----------------------------------------------------------
    
    @pyqtSlot()
    def inc(self): # For testing.
        self.i += 1
        self.managerInc.emit(self.i)
        return(self.i)

    @pyqtSlot()
    def send(self, val): # For testing.
        self.events.readflag.ignore()
        self.events.writeflag.accept()
        self.events.closeflag.ignore()

        self.q.put(val)


    @pyqtSlot()
    def setPort(self):
        pass # TODO: create a func to set the comport.
             # For now we'll harcode this into a constant. But, at some point
             # we need to create a settings form which we can adjust com
             # settings from. Will need to write to the settings port.
             # Maybe we just implement this from main()

    @pyqtSlot()
    def openPort(self): # This will be neccessary once we get a settings page
                        # Will need to be able to read from the settings file.
                        # For now, we'll just set an alias.
        #what do we need to do here...
        #first, we need to check to see if the comport is open and the thread is running
        #if the thread is running, we don't need to do anything.
        #if we do need to do something... I'm not sure what we need to do. Need to see
        #if we actually have to remake the worker, and thread , and move the worker and start the thread
        #or if we just start the thread or what.

        #This is breaking because we call this to setup the com port
        #before we setup the worker or thread...starting to think 
        #we need to leave as is and make another function to restart
        #stuff afterwards... need to think on this some

        try:
            ser = serial.Serial(SERIAL_PORT)
            self.comStatus.emit("open") if ser.is_open else self.comStatus.emit("closed")
            #print(ser.is_open)
            # self.worker_thread = QThread() #create a thread
            # self.worker.moveToThread(self.worker_thread) #move the worker to the thread
            #self.worker_thread.start() #start the thread
            return(ser)



        except serial.serialutil.SerialException:
            print("Serial error: ",sys.exc_info()[0])
            self.comStatus.emit("error")
            raise

    @pyqtSlot()
    def restartCom(self):
        if (not self.ser.is_open):
            self.ser.open()

            self.events.readflag.accept()
            self.events.writeflag.ignore()
            self.events.closeflag.ignore()

            self.worker_thread.start()

    @pyqtSlot()
    def close(self):
        self.events.readflag.ignore()
        self.events.writeflag.ignore()
        self.events.closeflag.accept()

    @pyqtSlot()
    def read(self):
        self.events.readflag.accept()
        self.events.writeflag.ignore()
        self.events.closeflag.ignore()

        #self.worker.run()

    #region -- unused write slot
    # @pyqtSlot()
    # def write(self):
    #     self.events.readflag.ignore()
    #     self.events.writeflag.accept()
    #     self.events.closeflag.ignore()
    #endregion

#endregion------------------------------------------------

#region - Worker Object -------------------------
# Create a Worker object that will be threaded and do the actual rading/writing
# To be run in thread. Creates a forever loop escaped by event flag
# Uses if, elif, else decision tree to find out what to do.
#------------------------------------------------
class Worker(QObject):
    dataReady = pyqtSignal(tuple)
    finished = pyqtSignal()
    comStatus = pyqtSignal(str)

    buffer = bytearray()

    def __init__(self, events, ser, q):
        super().__init__()
        self.readflag = events.readflag
        self.closeflag = events.closeflag
        self.writeflag = events.writeflag

        self.ser = ser
        self.q = q     

    def run(self):
        while(True):
            if(self.closeflag.isAccepted()): #Finished -> finished.emit()
                self.ser.close()
                self.comStatus.emit("open") if self.ser.is_open else self.comStatus.emit("closed")
                self.finished.emit()
                break
            elif(self.readflag.isAccepted()): #Read magic -> dataReady.emit(int)
                newByte = self.ser.read()
                
                if (newByte != b'\x00'):
                    self.buffer.extend(newByte)
                else:
                    try:
                        decoded = cobs.decode(self.buffer)

                        crc_recv = crc16.crc16xmodem(decoded[:-2]) #performs crc16 on all except for the last 2 bytes
                        crc_sent = struct.unpack("H", decoded[-2:])[0] #extracts the last 2 bytes in decoded, "H" is unsiged short - 2 bytes

                        if (crc_recv != crc_sent): 
                            print("crcError")
                            raise crcError

                        data = struct.unpack(RXPACKET_FORMAT, decoded)
                    
                    except cobs.DecodeError:
                        print("cobs decode error")
                    except crcError:
                        print("crc error")
                    except struct.error:
                        print("struct error")
                    except:
                        print("Error: ",sys.exc_info()[0])
                        raise

                    else:
                        self.dataReady.emit(data)


                    finally:
                        self.buffer.clear()
            elif(self.writeflag.isAccepted): #TODO: make this actually write something... need to go back to the arduino first
                # write some data
                print('writing data')
                key = 1
                print(key)
                value = int(self.q.get())
                print(value)
                crc = 0
                print(key, value, crc)
                strct = struct.pack("3H", *data) #"*" unpacks a list
                print(strct.key)
                # crc = crc16.crc16xmodem(key.to_bytes(2,"big"), 0)
                # crc = crc16.crc16xmodem(value.to_bytes(2,"big"), crc)
                # strct = cobs.encode(strct)
                print(strct)
                self.ser.write(cobs.encode(struct.pack("3H", key, value, crc)))

                
                # set back to reading mode
                self.readflag.accept()
                self.writeflag.ignore()

                continue
            else: #Continue looping
                continue
#endregion - Worker object -------------------------

#region - MyEvents object -----------------------
# Create an object, MyEvents() to hold custom event flags.
#------------------------------------------------
class MyEvents():
    def __init__(self):
        self.readflag = QEvent(QEvent.registerEventType()) #read=set, write=unset
        self.writeflag = QEvent(QEvent.registerEventType())
        self.closeflag = QEvent(QEvent.registerEventType()) #stop/close=set, run=unset

        self.readflag.accept() #set readflag to set - initially reading
        self.writeflag.ignore() #set writeflag to unset - initially reading, not writing
        self.closeflag.ignore() #set closeflag to unset - initially open port
#endregion - MyEvents object --------------------

#region - crcError object ------------------------
# Define an error handler for my crc check
#------------------------------------------------
class crcError(Exception):
    #TODO: maybe add some code that does something useful...I can't think of anything for now.
    pass
#endregion - crcError object ---------------------

#region - TODO: create a myserial class and overload the base serial class
# class myserial(serial):
#     __init__(self):
#     super.__init
#endregion