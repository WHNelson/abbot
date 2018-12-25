
#define TXPACKET_LEN  8     //number of bytes
#define RXPACKET_LEN  6     //number of bytes
#define CRC_INIT 0          //the initial value for the crc calculation


#include <RunningMedian.h>
#include <math.h>
#include <string.h>
#include <PacketSerial.h>
#include <Crc16.h>


//txpacket config
typedef union {
  struct {
    unsigned int seqnum;     //2 bytes 
    unsigned int distance;    //2 bytes
    unsigned int loopback;      //2 bytes
    unsigned int crc;          //2 bytes
  };
  byte bytes[TXPACKET_LEN];
} txPacket;

//rxpacket config
typedef union {
  struct {
    unsigned int key; //2 bytes
    unsigned int val; //2 bytes
    unsigned int crc; //2 bytes
  };
  byte bytes[RXPACKET_LEN];
} rxPacket;

//-------------------------------------
//setup variables
//-------------------------------------
//Setup RunningMedian
RunningMedian samples = RunningMedian(15);
//setup the pins
int Echo = A4;            //todo: figure out what this does
int Trig = A5;            //todo: figure out what this does
//define some variables to creat a low pass filter
//low pass filter: val = prev_val*k + reading*(k-1)
float k = 1.0;            //kalman gain -- this is how much we rely on prev val
//value to hold new reading
int new_val = 0;
//define data variable as Packet type
rxPacket rxdata;
txPacket txdata;
//setup test variable
int n = 0;
//setup PacketSerial
PacketSerial myPacketSerial;
//setup Crc
Crc16 crc;

//-------------------------------------
//ultrasonic distance measurement
//-------------------------------------
int DistanceTest(){
  digitalWrite(Trig, LOW);                //"primes" trigger output
  delayMicroseconds(5);
  digitalWrite(Trig, HIGH);               //trigger held high for 20us triggers measurement
  delayMicroseconds(20);
  digitalWrite(Trig, LOW);                //trigger pulled low to wait for echo
  float Fdistance = pulseIn(Echo, HIGH);  //waiting for pulseIn, Fdistance is float distance
  
  return (int)Fdistance;
}


//-------------------------------------
//read serial port using PacketSerial
//-------------------------------------
void onPacketReceived(const uint8_t* buffer, size_t size) {
  // Process decoded incoming packet here.
  rxdata.key = ((int)((buffer[0]) << 8) + buffer[1]);
  rxdata.val = ((int)((buffer[2]) << 8) + buffer[3]);
  rxdata.crc = ((int)((buffer[4]) << 8) + buffer[5]);
  
  switch (rxdata.key) {
    case 1: {
      k = rxdata.val/1000.0;
      break;
    }
  }
}

//-------------------------------------
//setup
//-------------------------------------
void setup(){
  //Serial.begin(9600);
  myPacketSerial.begin(9600);
  myPacketSerial.setPacketHandler(&onPacketReceived);
  
  pinMode(Echo, INPUT);    
  pinMode(Trig, OUTPUT);
}

//-------------------------------------
//main
//-------------------------------------
void loop(){
  
  //get a new reading
  new_val = DistanceTest();
  //if the value isn't 0 add it to the RunningMean samples
  if(new_val>0){
    samples.add(new_val);
  }
  //apply the kalman gain
  txdata.distance = txdata.distance*(1-k) + samples.getMedian()*(k);
 
  //update sequence number...this just counts up...an indicator of the number of loops so far
  txdata.seqnum = n++;
  
  //Do a CRC calculation
  txdata.crc = crc.XModemCrc(txdata.bytes, CRC_INIT, TXPACKET_LEN - 2);  //initialize crc to 0
   
  //write out the data using COBS from PacketSerial class 
  myPacketSerial.send(txdata.bytes,TXPACKET_LEN);
  
  //check for incoming data
  myPacketSerial.update();
  
  //loop back the received val
  txdata.loopback = int(k*1000);
  
  //wait for a sec... keep the comm buffers from overflowing
  delay(10);
}

