import sys
sys.path.append("../")
import math, collections, concurrent, time, cv2
import numpy as np

from typing import Tuple
from server.vision.camera import Camera
from server.vision.room import Room
from server.pathfinding.planner import AStarPlanner
from server.BaseComms import BaseComms
from multiprocessing import Process, Manager, Pool

class BaseCommand:
    __instance = None
    manager = Manager() 
    def __init__(self, interface, gx, gy):
        if self.__instance is not None:
            raise Exception("Singelton class")
        else:
            self.__instance = self

        self.obsts = Room('room0').obsts.values()
        self.camera = Camera(interface)
        self.rx, self.ry = None, None  # Path
        self.get_path(gx, gy)
        #Dummy path dictionary
        #TODO: This needs to be populated before use.
        self.paths = self.manager.dict()
        self.comms = BaseComms()
        self.tableMoveStage = collections.defaultdict(lambda : 0)
        # executer = concurrent.futures.ProcessPoolExecutor(10)
        # futures = [executer.submit(self.move, group) for group in grouper(5, )]
        pool = Pool()
        result_move = pool.map(self.move)
        result_transmit = pool.apply_async(self.comms.transmit())
        # self.move()

    def get_pos_orientation(self):
        pos = self.camera.get_pos(1)[1]
        return (pos[0] + pos[2]) / 2, pos[0] - pos[3]

    @ staticmethod
    def dist(pt1, pt2):
        return math.sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)

    # def move(self):
    #     for x, y in zip(self.rx, self.ry):
    #         cur_pos = self.get_pos_orientation()
    #         while BaseCommand.dist(cur_pos[0], (x, y)) > 36:
    #             self.move2Checkpoint(x, y, cur_pos)
    #             cur_pos = self.get_pos_orientation()

    #     return True

    def move(self):
        while self.paths:
            def helper_move():
                for table, checkpoint in self.paths.items():
                    cur_pos_dict = self.get_pos_orientation()
                    cur_pos = cur_pos_dict[table]
                    x, y = checkpoint[self.tableMoveStage[table]]

                    while BaseCommand.dist(cur_pos[0], (x, y)) < 36 and self.tableMoveStage[table] < len(checkpoint):
                        self.tableMoveStage[table] += 1
                        x, y = checkpoint[self.tableMoveStage[table]]

                    if self.tableMoveStage[table] == len(checkpoint):
                        # del self.tableMoveStage[table]
                        del self.paths[table]
                        continue

                    self.move2Checkpoint(x, y, cur_pos, table)
                    self.tableMoveStage[table] += 1
            helper_move()
            # pool = Pool()
            # result = pool.map(helper_move)

    def move2Checkpoint(self, table_id, x, y, cur_pos):
        robot_orientation = cur_pos[1]
        target_orientation = np.array((x - cur_pos[0][0], y - cur_pos[0][1]))
        if abs(BaseCommand.angle(robot_orientation, target_orientation)) > 15:
            print(BaseCommand.angle(robot_orientation, target_orientation), " ", 
            BaseCommand.cross(robot_orientation, target_orientation))
            if BaseCommand.cross(robot_orientation, target_orientation) > 0:
                self.comms.turnRight(table_id)
            else:
                self.comms.turnLeft(table_id)
            time.sleep(0.15)
        else:
            self.comms.goForward(table_id)
            time.sleep(0.35)
        self.comms.stop(table_id)
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

    #Gavin edited to be a dictionary. Key (tableID) -> Value (List of checkpoints.)
    def get_path(self, gx, gy):
        def getPath(sx, sy):
            nonlocal gx, gy
            ox, oy = [], []
            def drawRect(point0, point1) -> None:
                base = abs(point0[0] - point1[0])
                side = abs(point0[1] - point1[1])
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
            grid_size, robot_radius = 10.0, 105.0
            a_star = AStarPlanner(ox, oy, grid_size, robot_radius, True)
            rx, ry = a_star.planning(int(np.around(sx)), int(np.around(sy)), gx, gy)
            rx, ry = rx[::-1], ry[::-1]
            return rx, ry
        pos = self.camera.get_pos(1)[1]
        sx, sy = (pos[0] + pos[2]) / 2  #center
        self.rx, self.ry = getPath(sx, sy)


if __name__ == '__main__':
    # p = (570, 256)  # top
    # p = (1235, 563) # right
    p = (603, 889)  # bottom
    try:
        bc = BaseCommand(0, p[0], p[1])
    except Exception:
        print("In progress. Wait until process ends")
