#include "EEPROM.hpp"

//Arduino Uno has 1KB EEPROM storage.
//Only access to up to 512 bytes! (not clear why)

/*
 * EEPROM Clear
 *
 * Sets all of the bytes of the EEPROM to 0. (initially 255 if not written)
 * Use this before writing any data into the EEPROM
 *
 *The update function is used instead of the write as it check whether it already
 *has the same value or not, by the maximum erease and write cyclein mind
 */
void clearEEPROM() {
  //Iterate through each byte of the EEPROM storage.
  for (int i = 0 ; i < EEPROM.length() ; i++) {
    EEPROM.update(i, 0);
  }
}

/*
 * EEPROM Write
 *
 * Sets a single pre-assgned byte to the value recieved
 *
 * writeTo: address of the EEPROM to write to (use 0 - 512)
 * setTo: the value to be written to.
 *
 *The update function is being used for the same reason as it is for the clear
 */
void writeEEPROM(byte setTo, int writeTo) {
    EEPROM.update(writeTo, setTo);
}


/*
 * EEPROM read
 *
 * Reads the EEPROM at the defined address
 *
 * returns a byte of the value which was there.
 *
 */
 byte readEEPROM(int readFrom) {
     return EEPROM.read(readFrom);
 }

/*
 * set Table ID
 *
 * Sets the table ID, after clearing all the memory to 0s.
 *
 * tableID: the ID of the table calling this function. The byte value will be
 *          read from the EEPROM at a predefined address (found in EEPROM.hpp)
 *
 * The update function is being used for the same reason as it is for the clear
 */
void setTableID(byte tableID) {
    //clear the EEPROM, before setting the value. The is a fresh start.
    clearEEPROM();


    //write the address to the pre-assigned location
    writeEEPROM(TABLEID_EEPROM_ADDRESS, tableID);
}


/*
 * read Table ID
 *
 * Reads the table ID, should be used when it is started up
 *
 * returns: the ID of the table calling this function. The byte value will be
 *          read from the EEPROM at a predefined address (found in EEPROM.hpp)
 *
 */
byte readTableID() {

    //DO NOT USE 0 AS A TABLE ID, AS A CLEARED EEPROM WOULD SHOW 0 AS VALUE,
    //MEANING THAT IT WAS NOT SET!!!!
    return readEEPROM(TABLEID_EEPROM_ADDRESS);

}
