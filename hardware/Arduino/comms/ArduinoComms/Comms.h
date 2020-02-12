#ifndef Comms_h
#define Comms_h

#include "Arduino.h"

class Comms
{
    public:
        static void setupComms();
        static char* getPacket();
        static void showNewData();
        Comms() {};

    private:
        const static byte numChars;
        static char receivedChars[]; // an array to store the received data
        static bool newData;
        static void recvWithEndMarker();
};
#endif
