#include "Comms.h"
#include <Wire.h>
#include <SDPArduino.h>

Comms comms;
void setup()
{
  SDPsetup();
  comms.setupComms();
}

void loop()
{
  comms.getPacket();
  comms.showNewData();
}
