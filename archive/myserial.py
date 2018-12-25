    # def createThreading(self):
    #     print("threading")
    #     #Threading....
    #     #1. create our threaded worker
    #     self.wrkr = robotser.RSerial()
    #     #2. connect worker "ready" signal to our "onReady" slot
    #     self.wrkr.dataReady.connect(self.onReady)
    #     #3. create and move the worker object to a thread
    #     self.thread = QThread()
    #     self.wrkr.moveToThread(self.thread)
    #     #4. connect worker "finished" signal to the (built-in) thread quit slot
    #     #self.wrkr.finished.connect(self.thread.quit)
    #     #5. connect (built-in) thread started signal to the worker (doSomething) slot
    #     self.thread.started.connect(self.wrkr.comControl)
    #     #6. have the thread actually shutdown the app with a connection to app.exit
    #     #self.thread.finished.connect(app.exit)
    #     #7. actually start the thread... triggers thread.started
    #     self.thread.start()
    #     #continue main() code from here...


        # #class functions - ReadSerial
    # def ReadSerial(self):
    #     #define some variables for easier reading
    #     input_buff = self.input_buff
    #     packet_start = self.packet_start
    #     ser = self.ser
    #     struct_len = self.struct_len-4 #trim off our 4 byte packet start marker
        
    #-------------------------------------------    
    #     #read in a value and add it to the end of the buffer
    #     input_buff.extend(ser.read())
    #     #keep the buffer size at 4, pop the first element TODO: don't hard code this "4"
    #     if (len(input_buff) > 4): input_buff.pop(0)
    #     #check to see if we have a "start" sequence to mark the start of structured data
    #     if(input_buff == packet_start):
    #         #read and unpack the packet.. unpack returns a tuple
    #         val = unpack(PACKET_FORMAT,ser.read(struct_len))
    #         #update the text box
    #         self.distance.set(val[2])
    #         self.ser_waiting.set(ser.in_waiting)
            
    #         #clear the input buffer of anything else that might be there.. and to catch up
    #         #ser.reset_input_buffer()
    
    #     #place a callback back into the mainloop()
    #     self.frm_main.after(1, self.ReadSerial)

    """
    Note: use this to list the com ports
    from serial.tools.list_ports import comports
    then in the function test with
    for ports in comports(): print(ports)
    you may have to to split() on the return string to just get the comport bit.
    reference: https://github.com/pyserial/pyserial/blob/master/serial/tools/list_ports.py
    and the doc at: https://pyserial.readthedocs.io/en/latest/tools.html
    has... port.device, port.name, port.description, port.hwid,
      for usb.. port.vid, port.pid, port.serial_number, port.location, port.manufacturer, port.product, port.interface
    you can use from the command line with:
        pi@raspizero:~ $ python3 -m serial.tools.list_ports -v
            /dev/ttyAMA0        
                desc: ttyAMA0
                hwid: 3f201000.serial
            1 ports found
        pi@raspizero:~ $ python3 -m serial.tools.list_ports -h
            usage: list_ports.py [-h] [-v] [-q] [-n N] [regexp]

            Serial port enumeration

            positional arguments:
            regexp         only show ports that match this regex

            optional arguments:
            -h, --help     show this help message and exit
            -v, --verbose  show more messages
            -q, --quiet    suppress all messages
            -n N           only output the N-th entry

Look at this for some threading help:
https://github.com/pyserial/pyserial/blob/master/examples/wxTerminal.py
    """