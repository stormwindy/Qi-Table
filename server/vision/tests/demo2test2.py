import sys
sys.path.append("../../../")
import math
import time
import numpy as np
from server.vision.camera import Camera
from server.vision.room import Room
from server.pathfinding.planner import AStarPlanner
from server.BaseComms import BaseComms

class BaseCommand:

    def __init__(self, interface, gx, gy):
        self.obsts = Room('room0').obsts.values()
        self.camera = Camera(interface)
        self.rx, self.ry = None, None  # Path
        self.get_path(gx, gy)
        self.comms = BaseComms()
        self.move()

    def get_pos_orientation(self):
        t1 = time.time()
        pos = self.camera.get_pos(1)[1]
        t2 = time.time()
        print(t2-t1)
        return (pos[0] + pos[2]) / 2, pos[0] - pos[3]

    @ staticmethod
    def dist(pt1, pt2):
        return math.sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)

    def move(self):
        for x, y in zip(self.rx, self.ry):
            cur_pos = self.get_pos_orientation()
            while BaseCommand.dist(cur_pos[0], (x, y)) > 15:
                self.move2Checkpoint(x, y, cur_pos)
                cur_pos = self.get_pos_orientation()

    def move2Checkpoint(self, x, y, cur_pos):
        robot_orientation = cur_pos[1]
        target_orientation = np.array((x - cur_pos[0][0], y - cur_pos[0][1]))
        if abs(BaseCommand.angle(robot_orientation, target_orientation)) > 15:
            if BaseCommand.cross(robot_orientation, target_orientation) > 0:
                self.comms.turnRight()
            else:
                self.comms.turnLeft()
        else:
            self.comms.goForward()
        time.sleep(0.25)
        self.comms.stop()
        return


    @ staticmethod
    def cross(v1, v2):  # 2d vec should return 1d number
        v1, v2 = np.array(v1), np.array(v2)
        return np.cross(v1, v2)

    @ staticmethod
    def angle(v1, v2):  # degrees
        v1, v2 = np.array(v1), np.array(v2)
        nom = np.linalg.norm(BaseCommand.cross(v1, v2))
        denom = np.linalg.norm(v1)*np.linalg.norm(v2)
        return math.degrees(math.asin(nom/denom))

    def get_path(self, gx, gy):
        def getPath(sx, sy):
            nonlocal gx, gy
            ox, oy = [], []
            def drawRect(point0, point1) -> None:
                side = abs(point0[0] - point1[0])
                base = abs(point0[1] - point1[1])
                for xx in range(base):
                    ox.append(point0[0] + xx)
                    oy.append(point0[1])
                    ox.append(point0[0] + xx)
                    oy.append(point0[1] + side - 1)
                for yy in range(side):
                    oy.append(point0[1] + yy)
                    ox.append(point0[0])
                    oy.append(point0[1] + yy)
                    ox.append(point0[0] + base - 1)
            for pt1, pt2 in self.obsts:
                drawRect(pt1, pt2)
            grid_size, robot_radius = 30.0, 115.0
            a_star = AStarPlanner(ox, oy, grid_size, robot_radius)
            rx, ry = a_star.planning(int(np.around(sx)), int(np.around(sy)), gx, gy)
            rx, ry = rx[::-1], ry[::-1]
            return rx, ry
        pos = self.camera.get_pos(1)[1]
        sx, sy = (pos[0] + pos[2]) / 2  #center
        self.rx, self.ry = getPath(sx, sy)




if __name__ == '__main__':
    # p = (525, 564)  #left
    # p = (936, 296)  #top
    # p = (1337, 551)  #right occupied now
    p = (977,920)  #bottom
    bc = BaseCommand(1, p[0], p[1])
