#include "SDPArduino.h"
#include "NxtControl.h"
//#include <Wire.h>
#include <SoftwareSerial.h>

#define rxPin 10
#define txPin 11
//SoftwareSerial NxtControl::mySerial = SoftwareSerial(rxPin, txPin);

int NxtControl::i = 0;
byte NxtControl::rx_byte = 0;
char NxtControl::moveDirection = '5';
int NxtControl::power = 50;
char NxtControl::curDir = '5';

NxtControl::NxtControl(SoftwareSerial *ss)
{
 NxtControl::mySerial = ss; 
}

void NxtControl::setupMotors(){
  NxtControl::mySerial->begin(9600);
  mySerial->println("PRINT ");
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  SDPsetup();
  helloWorld();
}

/*
 * Use this method to set direction and speed from antoher file/code.
 */
void NxtControl::setDirection(char dir, int powerInput)
{
  if (dir != NxtControl::moveDirection)
  {
    NxtControl::moveDirection = dir;
  }
  
  if (power != powerInput)
  {
    power = powerInput; 
  }
  
//  if (curDir == moveDirection) {return;}
//  curDir = moveDirection;
  //Letter W/w. Move forward
  if (NxtControl::moveDirection == '2')
  {
    motorForward(0, power);
    motorForward(1, power);
  } 
  //Letter a/A. Left turn.
  else if (NxtControl::moveDirection == '3')
  {
    motorForward(0, power);
    motorBackward(1, power);
  }
  //Letter d/D. Right turn.
  else if (NxtControl::moveDirection == '4')
  {
    motorBackward(0, power);
    motorForward(1, power);
  }
  //Letter s/S. Rear movement
  else if (NxtControl::moveDirection == '1')
  {
    motorBackward(0, power);
    motorBackward(1, power);
  }
  //Letter q/Q. Stop movement.
  else if (NxtControl::moveDirection == '5')
  {
    motorAllStop();
  }
}

/*
 * As of now both checks software calls from moveDirection var, and serial port 115200
 * to set directoin. Default speed is 50%.
 */
void NxtControl::moveMotors() {
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

void NxtControl::keyboardControl()
{
  if (Serial.available()) 
  {
    rx_byte = Serial.read();
    //Letter w/W. Forward movement.
    if (rx_byte == 87 || rx_byte == 119)
    {
      moveDirection = 0;
      Serial.println("Forward move start.");
    } 
    //Letter a/A. Left turn.
    else if (rx_byte == 65 || rx_byte == 97)
    {
      moveDirection = 3;
    }
    //Letter d/D. Right turn.
    else if (rx_byte == 68 || rx_byte == 100)
    {
      moveDirection = 4;
    }
    //Letter s/S. Rear movement
    else if (rx_byte == 83 || rx_byte == 115)
    {
      moveDirection = 1;
    }
    //Any other character is STOP.
    else 
    {
      moveDirection = 5;
    }
  } 
}
