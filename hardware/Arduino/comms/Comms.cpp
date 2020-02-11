#include "Arduino.h"
#include "Comms.h"

class Comms
{
const byte numChars = 32;
char receivedChars[numChars]; // an array to store the received data

bool newData = false;

void setupComms() 
{
  Serial.begin(9600);
  Serial.println("<Arduino comms is ready>");
}

//This method is used to get the current packet as a char array.
char *getPacket()
{
  recvWithEndMarker();
  return receivedChars;
}

//Loads a data packet into a char array. Packets have to be terminated with end marker.
void recvWithEndMarker() 
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
    }
  }
}

//Used to display recieved data packet. Use for debugging/testing.
void showNewData() 
{
  if (newData == true) 
  {
    Serial.print("Current packer: ");
    Serial.println(receivedChars);
    newData = false;
  }
}
}
