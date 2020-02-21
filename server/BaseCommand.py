import sys
sys.path.append("../")
import math
import time
from typing import Tuple
from server.vision.camera import Camera
from server.vision.room import Room
from server.pathfinding.planner import AStarPlanner
from server.BaseComms import BaseComms


class BaseCommand:
    def __init__(self):
        self.cam = Camera(0)
        self.room = Room('room0')
        self.getPos()
        self.angle = self.calcOrientation()
        self.gx = 1500
        self.gy = 1500
        self.comms = BaseComms()

    '''
    Main control loop that moves the robot around. Outer for loop divides path into subtasks to direct the robot.
    '''
    def move(self):
        rx, ry = self.getPath(self.sx, self.sy, self.gx, self.gy)
        for i in range(len(rx)):
            minDist = self.getDistCurTarget(rx[i], ry[i])
            self.correctOrientation(rx[i], ry[i])

            while not self.inRange(rx[i], ry[i]):
                self.getPos()
                distance = self.getDistCurTarget(rx[i], ry[i])
                self.correctOrientation()

                minDist = distance
                self.comms.goForward()
            self.comms.stop()

            #self.correctOrientation(rx[i], ry[i])

    '''
    Updates the position information of the object.
    '''

    def getPos(self):
        markerDict = self.cam.get_pos(1, True)
        self.leftMarker = markerDict[0][0]
        self.rightMarker = markerDict[0][1]
        # self.leftMarker = (1920 - self.leftMarker[0], self.leftMarker[1])
        # self.rightMarker = (1920 - sself.rightMarker[0], self.rightMarker[1])
        self.sx = (self.leftMarker[0] + self.rightMarker[0]) / 2
        self.sy = (self.leftMarker[1] + self.rightMarker[1]) / 2

    '''
    Checks if the target is in acceptable range. If so returns true.
    '''

    def inRange(self, rx: int, ry: int) -> bool:
        if rx - 10 < self.sx and self.sx < rx + 10 and ry - 10 < self.sy and self.sy < ry + 10: return True
        return False

    '''
    Code that allows robot to correct its direction as it travels accross the field.
    '''
    def correctOrientation(self, rx: int, ry: int):
        direction = self.getDirection((self.sx, self.sy), (rx, ry))
        self.comms.stop()
        time.sleep(0.3)
        while direction - 2 > self.angle and self.angle > direction + 2:
            self.comms.turnRight()
            self.getPos()
            self.angle = self.calcOrientation()
            
        self.comms.stop()

    def getDistCurTarget(self, rx: int, ry: int) -> float:
        return math.sqrt((rx - self.sy)**2 + (ry - self.sy)**2)

    def calcOrientation(self) -> float:
        #TODO check if this works. Might have to change it to negative.
        return self.getDirection(self.leftMarker, self.rightMarker) + 90


    '''
    Gets direction of an object/target given two points with respect to principle axis. 0 points to "EAST"/"Right"
    '''
    def getDirection(self, source: Tuple[int], target: Tuple[int]) -> float :
        latLeft = math.radians(source[1])
        latRight = math.radians(target[1])
        x = math.cos(latRight) * math.sin(math.radians(target[0] - source[0]))
        y = math.cos(latLeft) * math.sin(latRight) - math.sin(latLeft) *\
            math.cos(latRight) * math.cos(math.radians(target[0] - source[0]))
        angle = (math.degrees(math.atan2(x, y))+360)%360
        return angle

    def getPath(self, sx: int, sy: int, gx: int, gy: int) -> Tuple[list, list]:
        ox, oy = [], []
        def drawRect(point0: Tuple[int, int], point1: Tuple[int, int]) -> None:
            side = abs(point0[0] - point1[0])
            base = abs(point0[1] - point1[1])
            for xx in range(base):
                ox.append(point0[0] + xx)
                oy.append(point0[1])
            for xx in range(base):
                ox.append(point0[0] + xx)
                oy.append(point0[1] + side - 1)
            for yy in range(side):
                oy.append(point0[1] + yy)
                ox.append(point0[0])
            for yy in range(side):
                oy.append(point0[1] + yy)
                ox.append(point0[0] + base - 1)

        #Draw obstacles
        for pt1, pt2 in self.room.obsts.values():
            drawRect(pt1, pt2)

        # start, goal
        grid_size = 32.0
        #Change margin of +10 if needed.
        robot_radius = 140.0

        ###
        # t1 = time.time()
        a_star = AStarPlanner(ox, oy, grid_size, robot_radius)
        # t2 = time.time()
        # print(t2 - t1)
        rx, ry = a_star.planning(sx, sy, gx, gy)
        # t3 = time.time()
        rx = rx[::-1]
        ry = ry[::-1]
        return (rx, ry)
