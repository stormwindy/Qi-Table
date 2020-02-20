#ifndef NXTCONTROL_H
#define NXTCONTROL_H

#include "Arduino.h"
#include <SoftwareSerial.h>
#include <Wire.h>


class NxtControl
{
public:
    void setupMotors();
    void setDirection(char dir, int powerInput);
    NxtControl(SoftwareSerial *ss);
    SoftwareSerial * mySerial;
    void keyboardControl();
    static void moveMotors();

private:
    static int i;
    static byte rx_byte;
    static char moveDirection;
    static int power;
    static char curDir;
};
#endif
