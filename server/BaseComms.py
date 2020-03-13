import sys
import serial
import platform
from multiprocessing import Process, Manager
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM

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

UDP_PORT = 5005

class BaseComms:
    __instance = None
    def __init__(self):
        if self.__instance:
            raise Exception("Singelton class")
        else:
            self.__instance = self
        with Manager as manager:
            self.packetQueue = manager.list()
        self.ser = None
        if platform.system() == 'Linux':
            self.ser = serial.Serial('/dev/ttyACM0', 115200)
        elif platform.system() == 'Darwin':
            self.ser = serial.Serial('/dev/cu.usbmodem0000011', 115200)
        else:
            exit(1)

        self.hostIP = gethostbyname('bellsprout.inf.ed.ac.uk')
        self.mySocket = socket(AF_INET, SOCK_DGRAM)

    @staticmethod
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

    def transmit(self):
        if not self.packetQueue:
            time.sleep(0.3)
        while self.packetQueue:
            packet = self.packetQueue.pop(0)
            print(packet)            
            self.ser.write(packet)
            self.mySocket.sendto(packet, (self.hostIP, UDP_PORT))


    def __addToQueue(self, table_id : int, command : chr = None):
        if command:
            str_table_id = str(table_id)
            if len(str_table_id) == 1:
                str_table_id = '0' + str_table_id
            packet = str_table_id + command + '\n'
            self.packetQueue.append(packet)
        # else:
        #     while(1):
        #         command = self.whichCommandNumber()
        #         command += '\n'
        #         self.ser.write(command)

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

    def turnRight(self, table_id : int):
        self.__addToQueue(table_id, '4')

    def turnLeft(self, table_id : int):
        self.__addToQueue(table_id, '3')

    def goForward(self, table_id : int):
        self.__addToQueue(table_id, '2')

    def goBackward(self, table_id : int):
        self.__addToQueue(table_id, '1')

    def stop(self, table_id : int):
        self.__addToQueue(table_id, '5')

    def read_packet(self):
        line = self.ser.readline()
        return line

