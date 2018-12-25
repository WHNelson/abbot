
import threading
import queue
import struct
import serial
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QEvent
from crc16 import crc16xmodem
from cobs import cobs
from binascii import hexlify

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_BAUDRATE = 9600
RXPACKET_FORMAT = "4H"
TXPACKET_FORMAT = "2H"
PACKET_TERMINATOR = b'\x00'


class RSerial(QObject):
    data_ready = pyqtSignal(list)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.revents = REvents() #create my events so that I have event flags
        self.write_q = queue.Queue() #create a queue to pass in write data
        self.ropen() #open the port and start the thread

    @pyqtSlot()
    def ropen(self, port=SERIAL_PORT, baud=SERIAL_BAUDRATE):
        try:
            self.ser = serial.Serial(port, baud)
        except:
            print("Failed to open comm port {}".format(str(self.ser)))
            raise
        else:
            self.revents.closeflag.ignore() #set the close flag for reading
            self.rthread = threading.Thread(target=self.rread) #make a thread
            self.rthread.start() #start the thread

    @pyqtSlot()
    def rclose(self):
        self.revents.closeflag.accept() #send a flag to the loop to stop
        self.rthread.join() #kill/wait till the thread has stopped
        self.ser.close() #close the serial port

    @pyqtSlot()
    def rwrite(self, data):
        data[1]=int(data[1]) #TODO: data validation, put in some better data validation
        self.write_q.put(data) #add the data to the write queue

    def rsend(self): 
        #using the rwite() to format the data and post it to the queue
        #using the rsend() to actually send it out the wire 
        data = self.write_q.get() #get the data from the queue
        self.ser.write(self.rpack(data)) #pack and send the data

    def rread(self):
        ser = self.ser
        stop = PACKET_TERMINATOR
        data = []

        while(True):
            #check to see if there is anything in the write queue
            if self.write_q.qsize() > 0:
                self.rsend()
            try:
                data = ser.read_until(stop) #reads until we get to the terminator
                data = cobs.decode(data[:-1]) #strips the zero off the end when decoding
                crc_calc = crc16xmodem(data[:-2],0) #calculates crc for all except last int (2 bytes)
                crc_recv = struct.unpack("H", data[-2:])[0] #unpacks and gets the last int (2 bytes)

                if (crc_calc != crc_recv):  #check to see if crc's match
                    raise crcError          #else raise data error
                                   
            except (cobs.DecodeError, crcError, struct.error): #catch data errors and print out a message.
                print("Data error")                            #then just continue on
            except:
                raise                                          #for other errors, break the program
            else:   #if no errors... we have good data
                data = list(struct.unpack(RXPACKET_FORMAT, data)) #unpack into a list
                data[-1] = ser.in_waiting #TESTING: replace crc with rx_buffer size
                # self.data = data #return the data to the class level?? don't really need to do this
                self.data_ready.emit(data) #emit a data read signal
            finally:
                if self.revents.closeflag.isAccepted(): #always check to see if the closeflag is set
                    self.finished.emit()    #TODO: do something with this signal
                    break
                pass
                
    def rpack(self, data):
        #This function expects a 2ea list of ints (2 bytes ea.) in a key-value
        # arraingment. A crc16 checksum will be appended  (making it 6 bytes). 
        # It then COBS encodes it appending a b'\x00' delimiter 
        # (making the total packet 8 bytes).
        crc = 0
        for item in data:
            crc = crc16xmodem(item.to_bytes(2, "little"), crc)
        data.append(crc)
        packed = struct.pack(">{}H".format(len(data)), *data)
        return cobs.encode(packed) + PACKET_TERMINATOR   # delimited = cobs.encode(packed) + b'\x00'
    def rformat(self, byte_array):
        # Takes in a byte array. Runs it through hexlify. Then formats in in croups of "step"
        # Returns string.
        # Start and stop are used to trim off the "b'<data>'"... the b and single quotes part
        start = 2
        tmp = str(hexlify(byte_array))
        stop = len(tmp)
        step = 2
        return(' '.join(tmp[i:i+step] for i in range(start, stop, step)))



class crcError(Exception):
    pass
class REvents():
    def __init__(self):
        self.closeflag = QEvent(QEvent.registerEventType()) #stop/close=set, run=unset

        self.closeflag.ignore() #set closeflag to unset - initially open port
