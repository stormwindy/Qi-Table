from unittest import TestCase
from server.BaseComms import BaseComms
import time
import random, string


class TestBaseComms(TestCase):

    def test_stop(self):
        comms = BaseComms()
        comms.goForward()
        comms.stop()

    def test_turnRight(self):
        comms = BaseComms()
        comms.turnRight()
        time.sleep(5)
        comms.stop()

    def test_turnLeft(self):
        comms = BaseComms()
        comms.turnRight()
        time.sleep(5)
        comms.stop()

    def test_goForward(self):
        comms = BaseComms()
        comms.goForward()
        time.sleep(2)
        comms.stop()

    def test_goBackward(self):
        comms = BaseComms()
        comms.goBackward()
        time.sleep(2)
        comms.stop()

    def test_same_turn_right(self):
        comms = BaseComms()
        comms.turnRight()
        time.sleep(2)
        comms.turnLeft()
        time.sleep(2)
        comms.stop()

    def test_same_turn_left(self):
        comms = BaseComms()
        comms.turnLeft()
        time.sleep(2)
        comms.turnRight()
        time.sleep(2)
        comms.stop()

    def test_there_and_back(self):
        comms = BaseComms()
        comms.goForward()
        time.sleep(4)
        comms.goBackward()
        time.sleep(4)
        comms.stop()

    def test_packet_success(self):
        comms = BaseComms()
        wrongPacket = 0
        for i in range(1000):
            def randString(length):
                return''.join(random.choice(string.ascii_lowercase) for i in range(length))

            max_length = 31 #bytes
            randomStr = randString(random.randint(1, max_length))
            comms._test_transmit(randomStr)
            time.sleep(0.2)
            retPacket = comms.read_packet()
            if retPacket != randomStr:
                wrongPacket += 1
        assert (wrongPacket, 0)