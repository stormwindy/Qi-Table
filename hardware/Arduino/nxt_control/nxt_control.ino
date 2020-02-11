#include "SDPArduino.h"
#include <Wire.h>
#include <SoftwareSerial.h>

#define rxPin 10
#define txPin 11

int i = 0;
SoftwareSerial mySerial =  SoftwareSerial(rxPin, txPin);
void setupMotors(){
  Serial.println("PRINT ");
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  mySerial.begin(115200);
  SDPsetup();
  helloWorld();
}

byte rx_byte = 0;
int moveDirection = 0;
int power = 50;

/*
 * Use this method to set direction and speed from antoher file/code.
 */
void setDirection(int dir, int powerInput)
{
  if (dir != moveDirection)
  {
    moveDirection = dir;
  }
  
  if (power != powerInput)
  {
    power = powerInput; 
  }
}

int curDir = 5;
/*
 * As of now both checks software calls from moveDirection var, and serial port 115200
 * to set directoin. Default speed is 50%.
 */
void moveMotors() {
  if (Serial.available()) 
  {
    rx_byte = Serial.read();
    //Letter w/W. Forward movement.
    if (rx_byte == 87 || rx_byte == 119)
    {
      moveDirection = 2;
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
  if (curDir == moveDirection) {return;}
  curDir = moveDirection;
  //Letter W/w. Move forward
  if (moveDirection == 2)
  {
    motorForward(0, power);
    motorForward(1, power);
  } 
  //Letter a/A. Left turn.
  else if (moveDirection == 3)
  {
    motorForward(0, power);
    motorBackward(1, power);
  }
  //Letter d/D. Right turn.
  else if (moveDirection == 4)
  {
    motorBackward(0, power);
    motorForward(1, power);
  }
  //Letter s/S. Rear movement
  else if (moveDirection == 1)
  {
    motorBackward(0, power);
    motorBackward(1, power);
  }
  //Letter q/Q. Stop movement.
  else
  {
    motorAllStop();
  }
}
