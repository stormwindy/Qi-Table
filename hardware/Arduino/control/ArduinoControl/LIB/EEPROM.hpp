#ifndef EEPROM_H //include guard
#define EEPROM_H

//#include <EEPROM.h> //standard library to access the EEPROM

//this stores the address in the EEPROM for the table ID
#define TABLEID_EEPROM_ADDRESS  77

void clearEEPROM();
void writeEEPROM(byte setTo, int writeTo);
byte readEEPROM(int readFrom);
void setTableID(byte tableID);
byte readTableID();

#endif
