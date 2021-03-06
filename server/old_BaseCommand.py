import sys
sys.path.append("../")
import math
import time
import numpy as np
from typing import Tuple
from server.vision.camera import Camera
from server.vision.room import Room
from server.pathfinding.planner import AStarPlanner
from server.BaseComms import BaseComms
import cv2

class BaseCommand:
    def __init__(self, interface, show=False):
        self.cam = Camera(interface)
        self.room = Room('room0')
        self.getPos()
        self.angle = self.calcOrientation()
        print("Current angle: ", self.angle)
        self.gx = 795
        self.gy = 246
        self.comms = BaseComms()
        self.rx, self.ry = self.getPath(self.sx, self.sy, self.gx, self.gy)
        # if show:
        #     self.show()
        time.sleep(1)
        self.move()

    # def show(self):
    #     cap = self.cam.capture
    #     fp, frame = cap.read()
    #     while fp:
    #         print(np.int32([list(zip(self.rx, self.ry))]))
    #         print(type(np.int32([list(zip(self.rx, self.ry))])))
    #         cv2.polylines(frame, np.int32([list(zip(self.rx, self.ry))]), False, (0, 255, 0), thickness=3)
    #         for pts in self.room.obsts.values():
    #             pts = np.array(pts)
    #             print(pts)
    #             cv2.rectangle(frame, tuple(pts[0]), tuple(pts[1]), (0, 0, 255), thickness=3)
    #         cv2.imshow('fame', frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #         fp, frame = cap.read()


    '''
    Main control loop that moves the robot around. Outer for loop divides path into subtasks to direct the robot.
    '''
    def move(self):
        rx, ry = self.rx, self.ry
        for i in range(len(rx)):
            #print(self.getDirection((self.sx, self.sy), (rx[i], ry[i])))
            self.correctOrientation(rx[i], ry[i])

            # while not self.inRange(rx[i], ry[i]):
            #     self.getPos()
            #     self.vector = self.getVector(self.marker[0], self.marker[2])
            #     self.distance = self.getDistCurTarget(rx[i], ry[i])
            #     # self.correctOrientation(rx[i], ry[i])
            #     time.sleep(0.3)
            #     self.comms.goForward()
            #     time.sleep(0.5)
            #     self.comms.stop()
            # self.comms.stop()

            #self.correctOrientation(rx[i], ry[i])

    '''
    Updates the position information of the object.
    '''

    def getPos(self):
        markerDict = self.cam.get_pos(1, False)
        self.marker = markerDict[1]
        # self.leftMarker = (1920 - self.leftMarker[0], self.leftMarker[1])
        # self.rightMarker = (1920 - sself.rightMarker[0], self.rightMarker[1])
        self.sx = (self.marker[0][0] + self.marker[2][0]) / 2
        self.sy = (self.marker[0][1] + self.marker[2][1]) / 2

    '''
    Checks if the target is in acceptable range. If so returns true.
    '''

    def inRange(self, rx: int, ry: int) -> bool:
        if self.distance < 35: return True
        return False

    '''
    Code that allows robot to correct its direction as it travels accross the field.
    '''
    def correctOrientation(self, rx: int, ry: int):
        direction = self.getDirection((self.sx, self.sy), (rx, ry))
        anglediff = self.getAngleDiff(self.angle, direction)
        while not (abs(anglediff < 10)):
            if anglediff < 0:
                self.comms.turnLeft()
            elif anglediff > 0:
                self.comms.turnRight()
            time.sleep(abs(anglediff) / 180 if abs(anglediff) > 55 else 0.3)
            self.comms.stop()
            time.sleep(0.2)
            self.getPos()
            self.angle = self.calcOrientation()
            direction = self.getDirection((self.sx, self.sy), (rx, ry))
            anglediff = self.getAngleDiff(self.angle, direction)

        print("Corrected angle")
        self.comms.stop()

    def getAngleDiff(self, source, target) -> float:
        diff = (math.degrees(target) - math.degrees(source) + 180) % 360 - 180
        return diff + 350 if diff < -180 else diff

    # def isTurnLeft(self, angle, touchAngle):
    #     diff = touchAngle - angle
    #     if diff < 0:
    #         diff += 360
    #     if diff < 180:
    #        return False
    #     else:
    #         return True

    def getDistCurTarget(self, rx: int, ry: int) -> float:
        return math.sqrt((rx - self.sy)**2 + (ry - self.sy)**2)

    def calcOrientation(self) -> float:
        #TODO check if this works. Might have to change it to negative.
        return self.getDirection(self.marker[0], self.marker[3])


    '''
    Gets direction of an object/target given two points with respect to principle axis. 0 points to "EAST"/"Right"
    '''
    def getDirection(self, source: Tuple[int], target: Tuple[int]) -> float :
        return (math.atan2(target[1] - source[1], target[0] - source[0]))

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
        rx, ry = a_star.planning(int(np.around(sx)), int(np.around(sy)), gx, gy)
        # t3 = time.time()
        rx = rx[::-1]
        ry = ry[::-1]
        return (rx, ry)


if __name__ == '__main__':
    bc = BaseCommand(0, True)
