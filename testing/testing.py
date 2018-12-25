from crc16 import crc16xmodem
import struct
from cobs import cobs
from binascii import hexlify
import serial
import time
import threading
import queue
import sys

SERIAL_PORT = '/dev/ttyACM0'
RXPACKET_FORMAT = "4H"
TXPACKET_FORMAT = "2H"
PACKET_TERMINATOR = b'\x00'


class crcError(Exception):
    pass

class RSerial(object):
    def __init__(self, port, q):
        self.port = port
        self.baudrate = 9600
        self.ser = None
        self.data = []
        self.write_queue = q
    def ropen(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            # self.ser.reset_input_buffer()
            return self.ser
        except:
            print("Failed to open comm port {}".format(str(self.ser)))
            raise
    def rclose(self):
        self.ser.close()
    def rwrite(self, data):
        # print("out_waiting is: ", self.ser.out_waiting)
        self.ser.write(self.rpack(data))

    def rread(self):
        ser = self.ser
        stop = PACKET_TERMINATOR
        data = []

        n=0
        while(True):
            n += 1
            if n > 100: #TESTING: putting in a break-out
                break

            #check to see if there is anything in the write queue
            #if there is, we take a break here to write out the data
            if self.write_queue.qsize() > 0:
                # print("getting from queueu: ")
                self.rwrite(self.write_queue.get())

            try:
                data = ser.read_until(stop)
                data = cobs.decode(data[:-1]) #strips the zero off the end when decoding

                crc_calc = crc16xmodem(data[:-2],0) #calculates crc for all except last byte
                crc_recv = struct.unpack("H", data[-2:])[0] #just unpacks and gets the last byte

                if (crc_calc != crc_recv):
                    raise crcError


            #region -- exceptions                   
            except cobs.DecodeError:
                print("cobs decode error")
                # data = []
                # continue
            except crcError:
                print("crc error -> crc_recv, crc_calc: ", crc_recv, crc_calc)
                # data = []
            except struct.error:
                print("struct error")
                # data = []
            except:
                raise
            else:
                data = list(struct.unpack(RXPACKET_FORMAT, data))
                data[-1] = ser.in_waiting #TESTING: replace crc with rx_buffer size
                # data.append(ser.in_waiting)
                # data.append(ser.out_waiting) #testing send buffer
                self.data = data #return the data to the class level
                print(data) #TESTING: printing the data to the screen
            finally:
                pass
            #endregion - exceptions
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
        # delimited = cobs.encode(packed) + b'\x00'
        return cobs.encode(packed) + b'\x00'

    def rformat(self, byte_array):
        start = 2
        tmp = str(hexlify(byte_array))
        stop = len(tmp)
        step = 2
        return(' '.join(tmp[i:i+step] for i in range(start, stop, step)))


def main():
    qwrite = queue.Queue()

    rser = RSerial(SERIAL_PORT, qwrite)
    rser.ropen()

    read_thread = threading.Thread(target=rser.rread)
    read_thread.start()

    # time.sleep(0.5)
    # qwrite.put([1, 123])


    for i in range(50):
        # print("in main {}th time in loop".format(i))

        qwrite.put([1, i])
        time.sleep(0.001)


    read_thread.join()
    rser.rclose()
    print("back in main: data is ", rser.data)
    print("Done....")
if __name__ == '__main__':
    main()
