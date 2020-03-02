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
        self.a_star = None
        self.get_path(gx, gy)

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
            for pt1, pt2 in self.obsts.values():
                drawRect(pt1, pt2)
            grid_size, robot_radius = 10.0, 105.0
            self.a_star = AStarPlanner(ox, oy, grid_size, robot_radius, True)
            rx, ry = self.a_star.planning(int(np.around(sx)), int(np.around(sy)), gx, gy)
            rx, ry = rx[::-1], ry[::-1]
            return rx, ry
        pos = self.camera.get_pos(1)[1]
        sx, sy = (pos[0] + pos[2]) / 2  #center
        self.rx, self.ry = getPath(sx, sy)


    def show(self):
        cap = self.camera.capture
        fp, frame = cap.read()
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 1280, 720)
        while fp:
            frame = cv2.undistort(frame, self.camera.mtx, self.camera.dist)
            self.draw_path(frame)
            self.draw_grid(frame)
            self.draw_obsts(frame)
            self.draw_arrow(frame)
            self.draw_arrow(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            fp, frame = cap.read()

    def draw_grid(self, frame):
        for x, y, b in self.a_star.get_grid():
            if b:
                cv2.circle(frame, (int(x), int(y)), 1, (0, 0, 255))
            else:
                cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 0))

    def draw_path(self, frame):
        # cv2.polylines(frame, np.int32([list(zip(self.rx, self.ry))]), False, (0, 255, 0), thickness=3)
        for x, y in zip(self.rx, self.ry):
            cv2.circle(frame, (int(x), int(y)), 4, (255, 0, 0))

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
    # p = (570, 256)  # top
    # p = (1235, 563) # right
    p = (603, 889)  # bottom
    v = Visualizer(1, p[0], p[1])
    v.show()

