#include "Comms.h"
#include "NxtControl.h"
#include <Wire.h>
#include <SDPArduino.h>
#include <SoftwareSerial.h>

SoftwareSerial ss(10, 11);
Comms comms;
NxtControl nxt(&ss);
void setup()
{
  SDPsetup();
  comms.setupComms();
  nxt.setupMotors();
}

void loop()
{
  char commandChar = comms.getCommand();
  //comms.showNewData();

  nxt.setDirection(commandChar, 75);
  nxt.moveMotors();
}
