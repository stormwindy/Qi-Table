#include "Security.hpp"


//array mapping recieved direction to real direction
char directionsDecoder[10];


/*
 * During the handshake, this will set up the encoded values
 *
 * handshake[]: is an array of the mapping of the values provided by the base
 *              eg.: [0] L0, [1] L9, [2] R7, ...
 *              This array should have at maximum 20 elements!
 *
 * If everything went well returns true, otherwise false
 *
 */
bool setUpEncodedDirections(char handshake[], byte handshakeSize) {
  for (byte i = 0; i < handshakeSize; i+=2) {

    char convertedToDirection = convertToDirection(handshake[i]);
    //return a distress signal if it cannot be converted
    if (convertedToDirection == 0) {
      return false;
    }

    /*
     * Add the encoded value as an index and the value is the actual translation
     * This is similar to a HashMap of int to char
     */
    directionsDecoder[(handshake[i + 1] - '0')] = convertedToDirection;
  }
}

/*
 * Convert the directions sent by the base to the chars.
 *
 * For example convert 'L' to '3', 'F' to '2', etc.
 *
 */
char convertToDirection(char toBeConverted) {
  switch (toBeConverted) {
    case 'B': return '1';
    case 'F': return '2';
    case 'L': return '3';
    case 'R': return '4';
    default : return 0; //if not either hence transmission error
  }
}

/*
 * ONLY RUN THIS IF THE setUpEncodedDirections WAS ALREADY EXECUTED!!!
 *
 * This method decodes the sent direction
 *
 * encodedDirection: is the char between '0' and '9', which can mapped to one of
 * the four directions (left: 3, right: 4, etc.)
 *
 * it returns the char of the direction (1 to 4), if ZERO is returned the program
 * is in distress as it cannot be mapped
 */
char getDirection(char encodedDirection) {

  byte tempIndex = encodedDirection - '0';
  if (tempIndex < 10 && tempIndex >= 0) {
    return directionsDecoder[tempIndex];
  }

  return 0;

}
