import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../..'))
from server.vision.camera import Camera
from server.vision.room import Room
from server.pathfinding.planner import AStarPlanner
import numpy as np
import cv2


class Visualizer:

    def __init__(self, interface, gx, gy):
        self.obsts = Room('room0').obsts
        self.camera = Camera(interface)
        self.rx, self.ry = None, None  #Path
        self.get_path(gx, gy)

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
            for pt1, pt2 in self.obsts.values():
                drawRect(pt1, pt2)
            grid_size, robot_radius = 30.0, 115.0
            a_star = AStarPlanner(ox, oy, grid_size, robot_radius)
            rx, ry = a_star.planning(int(np.around(sx)), int(np.around(sy)), gx, gy)
            rx, ry = rx[::-1], ry[::-1]
            return rx, ry
        pos = self.camera.get_pos(1)[1]
        sx, sy = (pos[0] + pos[2]) / 2  #center
        self.rx, self.ry = getPath(sx, sy)


    def show(self):
        cap = self.camera.capture
        fp, frame = cap.read()
        while fp:
            self.draw_path(frame)
            self.draw_obsts(frame)
            self.draw_arrow(frame)
            self.draw_arrow(frame)
            cv2.imshow('fame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            fp, frame = cap.read()

    def draw_path(self, frame):
        # cv2.polylines(frame, np.int32([list(zip(self.rx, self.ry))]), False, (0, 255, 0), thickness=3)
        for x, y in zip(self.rx, self.ry):
            cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0))

    def draw_obsts(self, frame):
        for pts in self.obsts.values():
            pts = np.array(pts)
            cv2.rectangle(frame, tuple(pts[0]), tuple(pts[1]), (0, 0, 255), thickness=3)

    def draw_arrow(self, frame):
        pos = self.camera.get_pos(1)[1]
        center = (pos[0] + pos[2]) / 2
        direction = pos[0] - pos[3]
        cv2.arrowedLine(frame, tuple(center), tuple(center + direction), (255, 0, 0), thickness=2)

if __name__ == '__main__':
    # p = (525, 564)  #left
    # p = (936, 296)  #top
    # p = (1337, 551)  #right occupied now
    p = (977, 920)  # bottom
    v = Visualizer(1, p[0], p[1])
    v.show()

