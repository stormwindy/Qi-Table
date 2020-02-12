#include "Arduino.h"
#include "Comms.h"

const byte Comms::numChars = 32;
char Comms::receivedChars[numChars]; // an array to store the received data

bool Comms::newData = false;

void Comms::setupComms() 
{
  Serial.begin(9600);
  Serial.println("<Arduino comms is ready>");
}

//This method is used to get the current packet as a char array.
char* Comms::getPacket()
{
  recvWithEndMarker();
  return receivedChars;
}

//Loads a data packet into a char array. Packets have to be terminated with end marker.
void Comms::recvWithEndMarker() 
{
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
  
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    
    if (rc != endMarker) 
    {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) 
      {
        Serial.write("Exceeded packet size limit.");
        ndx = numChars - 1;
      }
    }
    else 
    {
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true;
      Serial.println(receivedChars[ndx]);
    }
  }
}

//Used to display recieved data packet. Use for debugging/testing.
void Comms::showNewData() 
{
  if (newData == true) 
  {
    Serial.print("Current packet: ");
    Serial.println(receivedChars);
    newData = false;
  }
}

