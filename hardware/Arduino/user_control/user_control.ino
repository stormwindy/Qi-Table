#include "SDPArduino.h"
#include <Wire.h>
int motor1f = 10;
int motor1r = 11;

int motor2f = 5;
int motor2r = 6;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  helloWorld();
  pinMode(motor1f, OUTPUT);
  pinMode(motor1r, OUTPUT);
  pinMode(motor2f, OUTPUT);
  pinMode(motor2r, OUTPUT);
}

byte rx_byte = 0;
int moveDirection = 0;

void motorStop() 
{
  digitalWrite(motor1f, false);
  digitalWrite(motor2f, false); 
  digitalWrite(motor1r, false);
  digitalWrite(motor2r, false); 
}

void loop() {
  if (Serial.available()) 
  {
    rx_byte = Serial.read();

    if (moveDirection != 0) 
    {
      motorStop();  
    }
    //Letter w/W. Forward movement.
    if (rx_byte == 87 || rx_byte == 119)
    {
      moveDirection = 1;
      Serial.println("Forward move start.");
      digitalWrite(motor1f, true);
      digitalWrite(motor2f, true);
    } 
    //Letter a/A. Left turn.
    else if (rx_byte == 65 || rx_byte == 97)
    {
      moveDirection = 2;
      digitalWrite(motor1f, true);
      digitalWrite(motor2r, true);
    }
    //Letter d/D. Right turn.
    else if (rx_byte == 68 || rx_byte == 100)
    {
      moveDirection = 3;
      digitalWrite(motor1r, true);
      digitalWrite(motor2f, true);
    }
    //Letter s/S. Rear movement
    else if (rx_byte == 83 || rx_byte == 115)
    {
      moveDirection = 4;
      digitalWrite(motor1r, true);
      digitalWrite(motor2r, true);
    }
    //Letter q/Q. Stop movement.
    else if(rx_byte == 113 || rx_byte == 81)
    {
      motorStop();
    }
  }
}
