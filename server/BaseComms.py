import sys
import serial

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
        self.ser = serial.Serial('/dev/ttyACM0', 115200)

    def whichCommandNumber(key) -> chr:
        switcher = {
            'w':1,
            's':2,
            'a':3,
            'd':4,
            'p':5
        }
        return switcher.get(key)+'/n'


    def getKey(self):
        key = ''
        while not(key=='w' or key=='a' or key=='s' or key=='d' or key=='p'):
            key = input().lower()
            if not(key=='w' or key=='a' or key=='s' or key=='d' or key=='p'):
                print("Try Again")
        return key


    def keyboardControl(self):
        key = self.getKey()
        return self.whichCommandNumber(key)

    def transmit(self, command = None):
        print(self.ser.name)
        if command:
            command += '\n'
            self.ser.write(command)
        else:
            while(1):
                command = self.whichCommandNumber()
                command += '\n'
                self.ser.write(command)
