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
        char static receivedChars[]; // an array to store the received data
        bool static newData;
        static void recvWithEndMarker();
};
#endif
