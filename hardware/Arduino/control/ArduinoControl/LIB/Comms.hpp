#ifndef Comms_h
#define Comms_h

#include "Arduino.h"
#include <SoftwareSerial.h>

class Comms
{
    public:
        static void setupComms();
        static char* getPacket();
        static void showNewData();
        static char getCommand();
        Comms() {};

    private:
        static SoftwareSerial mySerial; 
        const static byte numChars;
        static int lastIndex;
        static char receivedChars[]; // an array to store the received data
        static bool newData;
        static void recvWithEndMarker();
};
#endif
