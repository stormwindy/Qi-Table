#include "CheckSum.hpp"
/*
 * This method returns true if the calculated checksum equals to the one
 * transmitted in the last char (using modulo-10).
 *
 * fullPacket: contains the chars transitted without the end market
 * packetSize: is the lenght of the fullPacket array
 *             (if max index = 2, size = 3)
 *
 */

bool compareCheckSum(char fullPacket[], char packetSize) {

  //store the sum of all numChars
  int sum = 0;

  //up until the character before the checksum
  for (byte i = 0; i < packetSize - 1; i++) {
    sum += (int)fullPacket[i];
  }

  /*
   * if the sum of the module-10 is the same as the last char in the transmittion
   * Please note that all chars is expected to be chars and not bytes, so the
   * checksum char is expected to be a char between '0' and '9', this meand that
   * by - '0' (as per ASCII table), we would get a digit.
   *
   */
  return ((sum % 10) == (fullPacket[packetSize - 1] - '0'));

}
