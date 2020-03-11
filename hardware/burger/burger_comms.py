import sys, socket
from config import DEVICE_ID
UDP_PORT = 5005
class Burger_Comms:
    def __init__(self):
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mySocket.bind(("", UDP_PORT))

    def get_payload(self):
        packet, addr = self.mySocket.recvfrom(4)
        if DEVICE_ID != packet[:2]:
            return None
        return packet[2] 
        

