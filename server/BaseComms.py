import sys
import serial
import platform

# def whichCommand(key):
#     switcher = {
#         'w':1,
#         's':2,
#         'a':3,
#         'd':4,
#         'p':5
#     }
#     numb = switcher.get(key)
#     return "echo -ne '{0}/n' > /dev/ttyACM0".format(numb)
class BaseComms:

    def __init__(self):
        self.ser = None
        if platform.system() == 'Linux':
            self.ser = serial.Serial('/dev/ttyACM0', 115200)
        elif platform.system() == 'Darwin':
            self.ser = serial.Serial('/dev/cu.usbmodem0000011', 115200)
        else:
            exit(1)


    def _whichCommandNumber(key) -> chr:
        switcher = {
            'w':1,
            's':2,
            'a':3,
            'd':4,
            'p':5
        }
        return switcher.get(key)+'/n'


    def _getKey(self):
        key = ''
        while not(key=='w' or key=='a' or key=='s' or key=='d' or key=='p'):
            key = input().lower()
            if not(key=='w' or key=='a' or key=='s' or key=='d' or key=='p'):
                print("Try Again")
        return key


    def _keyboardControl(self):
        key = self.getKey()
        return self.whichCommandNumber(key)

    def _transmit(self, command : chr = None):
        if command:
            command += '\n'
            self.ser.write(command.encode())
        else:
            while(1):
                command = self.whichCommandNumber()
                command += '\n'
                self.ser.write(command)

    def _test_transmit(self, command):
        if command:
            command += '\n'
            self.ser.write(command.encode())
        else:
            while(1):
                command = self.whichCommandNumber()
                command += '\n'
                self.ser.write(command)

    '''
    Interfacing methods for turning. If you are planning to transmit something other than following, add your own 
    public method. DO NOT use previous methods in this file outside of this class.
    '''

    def turnRight(self):
        self._transmit('4')

    def turnLeft(self):
        self._transmit('3')

    def goForward(self):
        self._transmit('2')

    def goBackward(self):
        self._transmit('1')

    def stop(self):
        self._transmit('5')

    def read_packet(self):
        line = self.ser.readline()
        return line

