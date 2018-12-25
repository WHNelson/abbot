from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread, QEvent
import sys
import time
import struct
import serial
from cobs import cobs
import binascii
import crc16



#define some constants
PACKET_START = b'STRT'
PACKET_STOP = b'\x0A'
PACKET_LEN = 6 #total len has a header added to it... so PACKET_LEN+(1 - 4) for header
PACKET_FORMAT = "4B2H"
SERIAL_PORT = '/dev/ttyACM0'

class Manager(QObject):
    managerInc = pyqtSignal(int)
    dataReady = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.i = 0

        #----------------------
        self.events = MyEvents()  #create some events
        self.reader = Reader(self.events) #create a reader with events
        self.reader.dataReady.connect(self.dataReady) #forward up the signal

        #----------------------
        self.readThread = QThread() #create a thread
        self.reader.moveToThread(self.readThread) #use the object.moveToThread to move the reader to the thread

        #----------------------
        self.reader.finished.connect(self.readThread.quit) #tie the fnished event to quit to stop the thread

        #----------------------
        self.readThread.started.connect(self.reader.read_proc) #connect the started signal to the starting function
        self.readThread.start() #start the thread


    @pyqtSlot() #called by the manager function
    def inc(self):
        self.i += 1
        self.managerInc.emit(self.i)
        return(self.i)

    @pyqtSlot() #used to toggle the event object used to pause the read loop
    def pauseReader(self):
        event = self.events.read
        event.ignore() if event.isAccepted() else event.accept()

    @pyqtSlot() #used to stop the reader, and stop the thread
    def stopReader(self):
        self.events.stop.accept()

    @pyqtSlot() #used to start the reader
    def startReader(self):
        self.events.read.accept()
        self.events.stop.ignore()

        self.readThread.start()
    

class MyEvents(): #used only to organze the custom events
    def __init__(self):
        self.read = QEvent(QEvent.registerEventType())
        self.stop = QEvent(QEvent.registerEventType())

        self.read.accept() #initially reading
        self.stop.ignore()

class Reader(QObject):
    dataReady = pyqtSignal(int)
    finished = pyqtSignal()

    ser = serial.Serial(SERIAL_PORT)
    buff = bytearray()

    def __init__(self, events):
        super().__init__()
        self.read = events.read
        self.stop = events.stop

    # def myread(self):
    #     newByte = self.ser.read()

    #     if (newByte != b'\x00'): 
    #         self.buff.extend(newByte)
    #     else:
    #         try:
    #             decoded = cobs.decode(self.buff)

    #             dataBuff = decoded[:-2]
    #             crcBuff = decoded[-2:]
                
    #             crcData = crc16.crc16xmodem(dataBuff)
    #             crcCalc = struct.unpack("H", crcBuff[0])

    #             if (crcData != crcCalc):
    #                 raise crcError

    #             data = struct.unpack(PACKET_FORMAT, dataBuff)

    #         except cobs.DecodeError:            #catch a cobs decoding error
    #             print("cobs.DecodeError")
    #         except crcError:                  #catch crc error
    #             print("crc error")
    #         except struct.error:                #catch an unpack error
    #             print("struct.error")
    #         except:                             #catch general error
    #             print("decoded length: {}".format(len(decoded)))
    #             print("Error:", sys.exc_info()[0])
    #             raise

    #         else:                        
    #             self.dataReady.emit(data[2])         #return the data
    #         finally:
    #             self.buff.clear()                #regardless, clear the buffer to ready for the next packet


    def read_proc(self):
        n = 0
        while(True):
            if(self.stop.isAccepted()):
                self.finished.emit()
                break
            elif(self.read.isAccepted()):
                n += 1
                time.sleep(0.1)
                self.dataReady.emit(n)
            else:
                continue

#define an error handler for my crc check later
class crcError(Exception):
    #TODO: maybe add some code that does something useful...I can't think of anything for now.
    pass

class RSerial(QObject):
    #setup signals
    #inReading = pyqtSignal() #signal to show that we're reading serail data
    dataReady = pyqtSignal(tuple) #signal to show that we have received data, using dict to xfer
    comStatus = pyqtSignal(bool) #signal to show com port state, whether opened or closed

    def __init__(self):
        super().__init__()
        #variables
        self.ser = serial.Serial(SERIAL_PORT)

        self.input_buff = bytearray()
        self.reading = False


    def comControl(self):
        print("comcontrol thread")

    def myread(self, ser):
        buff=self.input_buff  #TEMP: just going to define this to make it easier to read belowwhile(self.reading):
            #print("ser.in_waiting: ", self.ser.in_waiting, "bff len: ", len(buff))  
            #read a new byte
        in_waiting = ser.in_waiting
        print("in read()...{} bytes in waiting.".format(in_waiting))

        while(True):    #this is a blocking function...for the whole thread!!...need to make this it's own thread
            new_byte = ser.read() #read a new byte

            if (new_byte != b'\x00'):       #if not end of packet, add the new value to the buffer
                buff.extend(new_byte)       
            else:                           #else, we've got a packet, process it -> returns tuple(data)
                #DEBUG: parse bytearray into a list with uppercase hex values so that we can print them out
                try:
                    #DEBUG: we need to decode the buff...
                    #TODO: there's probably a more elegant way of doing this...
                    decoded = cobs.decode(buff)                 #cobs decode the buffer

                    data_buf = decoded[:-2]                     #extract the data portion -> bytearray
                    crc_buf = decoded[-2:]                      #extract the crc portion  -> bytearray

                    crc_data = crc16.crc16xmodem(data_buf)      #calculate the crc of the data -> int (2 bytes)
                    crc_calc = struct.unpack("H",crc_buf)[0]    #unpack the crc, get the int -> int (2 bytes)

                    #print(crc_data, crc_calc)
                    if (crc_data != crc_calc):
                        raise crcError     

                    data = struct.unpack("4B2H",data_buf)       #we've got a good packet, unpack -> tuple

                except cobs.DecodeError:            #catch a cobs decoding error
                    print("cobs.DecodeError")
                except crcError:                  #catch crc error
                    print("crc error")
                except struct.error:                #catch an unpack error
                    print("struct.error")
                except:                             #catch general error
                    print("decoded length: {}".format(len(decoded)))
                    print("Error:", sys.exc_info()[0])
                    raise

                else:                        
                    return data          #return the data
                finally:
                    buff.clear()                #regardless, clear the buffer to ready for the next packet
