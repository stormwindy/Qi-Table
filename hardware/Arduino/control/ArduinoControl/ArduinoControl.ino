#include "SDPArduino.h"
//#include "Comms.h"
//#include "NxtControl.h"
#include <Wire.h>
#include <SoftwareSerial.h>
#include <string.h>
#define rxPin 10
#define txPin 11

const byte numChars = 3;
char receivedChars[numChars]; // an array to store the received data
char moveDirection = '5';
char curDir = '5';
bool newData = false;
int lastIndex = 0;
String table_id = "01";
String commands = "012345";
//SoftwareSerial ss(10, 11);
//Comms comms;
//NxtControl nxt(&ss);

void setup()
{
  Serial.begin(9600);
  SDPsetup();
  //comms.setupComms();
  //nxt.setupMotors();
  Serial.println("Hello world");
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
}

void loop()
{
  char commandChar = getCommand();
  //comms.showNewData();
  if (commandChar == nullptr) {return;}
  setDirection(commandChar, 32);
  moveMotors();
}

char getCommand()
{
  recvWithEndMarker();
  //if (packet == NULL) {return NULL;}
  //showNewData();
  newData = false;
  if (table_id != receivedChars.substring(0, 2))
  {
    return nullptr;
  }
  return receivedChars[lastIndex - 1];
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

int power = 32;
void setDirection(char dir, int powerInput)
{
  if (dir != moveDirection)
  {
    moveDirection = dir;
  }
  
  if (power != powerInput)
  {
    power = powerInput; 
  }
  
  //if (curDir == moveDirection) {return;}
  curDir = moveDirection;
  //Letter W/w. Move forward
  if (moveDirection == '2')
  {
    motorForward(0, power);
    motorForward(1, power);
  } 
  //Letter a/A. Left turn.
  else if (moveDirection == '3')
  {
    motorForward(0, power);
    motorBackward(1, power);
  }
  //Letter d/D. Right turn.
  else if (moveDirection == '4')
  {
    motorBackward(0, power);
    motorForward(1, power);
  }
  //Letter s/S. Rear movement
  else if (moveDirection == '1')
  {
    motorBackward(0, power);
    motorBackward(1, power);
  }
  //Letter q/Q. Stop movement.
  else if (moveDirection == '5')
  {
    motorAllStop();
  }
}

void moveMotors() 
{
  if (curDir == moveDirection) {return;}
  curDir = moveDirection;
  //Letter W/w. Move forward
  if (moveDirection == '2')
  {
    motorForward(0, power);
    motorForward(1, power);
  } 
  //Letter a/A. Left turn.
  else if (moveDirection == '3')
  {
    motorForward(0, power);
    motorBackward(1, power);
  }
  //Letter d/D. Right turn.
  else if (moveDirection == '4')
  {
    motorBackward(0, power);
    motorForward(1, power);
  }
  //Letter s/S. Rear movement
  else if (moveDirection == '1')
  {
    motorBackward(0, power);
    motorBackward(1, power);
  }
  //Letter q/Q. Stop movement.
  else if (moveDirection == '5')
  {
    motorAllStop();
  }
}
