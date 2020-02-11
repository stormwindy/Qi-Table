#ifndef Comms_h
#define Comms_h

#include "Arduino.h"

class Comms
{
    public:
        static void setupComms();
        static char* getPacket();
        static void showNewData();

    private:
        const byte numChars = 32;
        char receivedChars[numChars]; // an array to store the received data
        bool newData = false;
        static void recvWithEndMarker();
        Comms() {};
}
#endif
