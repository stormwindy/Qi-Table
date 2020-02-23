#include "SDPArduino.h"
#include <Wire.h>
#include <SoftwareSerial.h>
#include <string.h>
#define rxPin 10
#define txPin 11

const byte numChars = 3;
char receivedChars[numChars]; // an array to store the received data
bool newData = false;
int lastIndex = 0;
String commands = "012345";
//SoftwareSerial ss(10, 11);
//Comms comms;
//NxtControl nxt(&ss);

void setup()
{
  Serial.begin(9600);
  SDPsetup();
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
}

void loop()
{
  recvWithEndMarker();
  char *packet = receivedChars;
  Serial.write(packet);
  Serial.write("\n");
  newData = false;
  //comms.showNewData();
}

void recvWithEndMarker() 
{
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
  
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    
    if (rc != endMarker && commands.indexOf(rc) != -1 ) 
    {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) 
      {
        Serial.write("Exceeded packet size limit.");
        ndx = 0;
      }
    }
    else 
    {
      receivedChars[ndx] = '\0'; // terminate the string
      lastIndex = ndx;
      ndx = 0;
      newData = true;
    }
  }
}
