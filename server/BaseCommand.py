import sys
sys.path.append("../")
import math
from typing import Tuple
from server.vision.camera import Camera
from server.vision.room import Room
from server.pathfinding.planner import AStarPlanner


class BaseCommand:
    def __init__(self):
        self.cam = Camera(0)
        room = Room('room0')
        markerDict = self.cam.get_pos(1, True)
        self.leftMarker = markerDict[0][0]
        self.rightMarker = markerDict[0][1]
        self.sx = self.leftMarker[0] + self.rightMarker[0]
        self.sy = self.leftMarker[1] + self.rightMarker[1]
        self.angle = self.calcOrientation()
        self.gx = 1500
        self.gy = 1500

    def move(self):
        rx, ry = self.getPath(self.sx, self.sy, self.gx, self.gy)
        for i in range(len(rx)):
            minDist = self.getDistCurTarget(rx[i], ry[i])
            direction = self.getDirection((self.sx, self.sy), (rx[i], ry[i]))
            self.correctOrientation(rx[i], ry[i])
            #TODO: stop

            while not self.inRange(rx[i], ry[i]):
                self.getPos()
                distance = self.getDistCurTarget(rx[i], ry[i])
                if distance > minDist:
                    self.correctOrientation()
                    #TODO: Stop
                minDist = distance
                #TODO: move forward
            #TODO: Stop

            #self.correctOrientation(rx[i], ry[i])

    def getPos(self):
        markerDict = self.cam.get_pos(1, True)
        self.leftMarker = markerDict[0][0]
        self.rightMarker = markerDict[0][1]

    def inRange(self, rx: int, ry: int):
        if rx - 10 < self.sx and self.sx < rx + 10 and ry - 10 < self.sy and self.sy < ry + 10: return True
        return False

    def correctOrientation(self, rx: int, ry: int):
        direction = self.getDirection((self.sx, self.sy), (rx, ry))
        while direction - 2 > self.angle and self.angle > direction + 2:
            self.getPos()
            self.angle = self.calcOrientation()
            # TODO: TURN RIGHT.
            pass

    def getDistCurTarget(self, rx: int, ry: int):
        return math.sqrt((rx - self.sy)**2 + (ry - self.sy)**2)

    def calcOrientation(self):
        return self.getDirection(self.leftMarker, self.rightMarker)

    def getDirection(self, source: Tuple[int], target: Tuple[int]):
        latLeft = math.radians(source[1])
        latRight = math.radians(target[1])
        x = math.cos(latRight) * math.sin(math.radians(target[0] - source[0]))
        y = math.cos(latLeft) * math.sin(latRight) - math.sin(latLeft) *\
            math.cos(latRight) * math.cos(math.radians(target[0] - source[0]))
        angle = (math.degrees(math.atan2(x, y))+360)%360
        return angle

    def getPath(self, sx: int, sy: int, gx: int, gy: int) -> Tuple[list, list]:
        ox, oy = [], []
        def draw_rect(x, y, lside, sside):
            # bot
            for xx in range(lside):
                ox.append(x + xx)
                oy.append(y)
            for xx in range(lside):
                ox.append(x + xx)
                oy.append(y + sside - 1)
            for yy in range(sside):
                oy.append(y + yy)
                ox.append(x)
            for yy in range(sside):
                oy.append(y + yy)
                ox.append(x + lside - 1)

        draw_rect(200, 300, 100, 200)
        draw_rect(600, 700, 200, 200)
        draw_rect(0, 0, 1920, 1080)
        draw_rect(1000, 200, 300, 300)
        draw_rect(1500, 700, 50, 50)
        # start, goal
        grid_size = 100.0
        robot_radius = 15.0

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
