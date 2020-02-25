
import numpy as np
import numpy.linalg as la
from math import *
import sys
sys.path.append("..\\..\\")
from server.vision.camera import Camera
from server.vision.room import Room
from base import *
from server.common.graphics import GraphWin, Transform
from sympy import Polygon, Point2D

class Planner:

    KP = 5
    ETA = 100

    def __init__(self, room_width, room_height):
        self.number_of_tables = None
        # self.camera = Camera(0)
        self.room_width = room_width
        self.room_height = room_height
        # self.ox, self.oy, self.orad = self.get_static_obstacles(Room(0).obsts)
        self.ox, self.oy, self.orad = self.get_static_obstacles(self.set_static_obstacles())
        self.tables = self.set_table_centres()
        goals = self.set_goal_coords()
        self.tables_to_goals(goals)
        self.path = []
        print(self.path)
        # self.draw()

    def get_table_centres(self, table_id, pos):

        """
        get_table_centres: returns centre of the specified table, and the list of other table centres excluding
        one that was specified

        :param table_id : id of the table that should not be included in the list
        :param pos: dictionary of table id's & ar tag positions
        :rtype: point, [point], point
        """

        # calculates the new obstacles(table_centres)
        tx = []
        ty = []
        for id in pos:
            # centre = [x, y]
            centre = (pos[id][0] + pos[id][2]) / 2
            if id == table_id:
                cx = centre[0]
                cy = centre[1]
                orientation = pos[id][0] - pos[id][3]
            else:
                tx.append(centre[0])
                ty.append(centre[1])

        return cx, cy, orientation, tx, ty

    def calc_attractive_potential(self, x, y, gx, gy):
        return 0.5 * self.KP * np.hypot(x - gx, y - gy)

    def calc_repulsive_potential(self, x, y, ox, oy, rr):

        safe_radius = rr

        # search nearest dynamic obstacle
        minid_d = -1
        dmin_d = float("inf")
        for i, _ in enumerate(ox):
            d = np.hypot(x - ox[i], y - oy[i])
            if dmin_d >= d:
                dmin_d = d
                minid_d = i

        # search nearest static obstacle
        minid_s = -1
        dmin_s = float("inf")
        for i, _ in enumerate(self.ox):
            d = np.hypot(x - self.ox[i], y - self.oy[i])
            if dmin_s >= d:
                dmin_s = d
                minid_s = i

        # dynamic obstacle is closer
        if dmin_s >= dmin_d:
            # calc repulsive potential
            dq = np.hypot(x - ox[minid_d], y - oy[minid_d])
            # safe distance between tables (distance between tables is the distance btw their centres)
            safe_radius = rr * 2
        # static obstacle is closer
        else:
            # calc repulsive potential
            dq = np.hypot(x - self.ox[minid_s], y - self.oy[minid_s])
            # safe distance = obstacle radius + robot radius
            safe_radius = self.orad[minid_s] + rr

        if dq <= (safe_radius):
            if dq <= 0.1:
                dq = 0.1
            return 0.5 * self.ETA * (1.0 / dq - 1.0 / safe_radius) ** 2
        else:
            return 0.0

    def next_cell(self, cell_x, cell_y, gx, gy, ox, oy, reso, rr):

        # adds room boundaries: table centre position can't come closer to the wall than its radius
        grid_bound_left = int(round(rr / reso))  # number of cells the radius takes
        grid_bound_right = int(round(self.room_width / reso - rr / reso))
        grid_bound_top = int(round(rr / reso))
        grid_bound_bottom = int(round(self.room_height / reso - rr / reso))

        minix, miniy = -1, -1
        minuf = float("inf")
        for ix in range((cell_x - 1), (cell_x + 2)):
            x = ix * reso
            for iy in range((cell_y - 1), (cell_y + 2)):
                y = iy * reso
                if ix <= grid_bound_right and ix >= grid_bound_left \
                        and iy <= grid_bound_bottom and iy >= grid_bound_top:
                    ug = self.calc_attractive_potential(x, y, gx, gy)
                    uo = self.calc_repulsive_potential(x, y, ox, oy, rr)
                    uf = ug + uo
                if minuf > uf:
                    minuf = uf
                    minix = ix
                    miniy = iy

        return minix, miniy

    # def move(self, id, x, y, cx, cy, orientation):
    #
    #     self.update_table(id, x, y, cx, cy, orientation)


    def multi_path(self, goals):

        # goals = dictionary which maps table id with its goal

        reso = 10
        rr = 115.0

        # pos = self.camera.get_pos(self.number_of_tables)
        pos = self.tables
        # iterate through tables
        for id in pos:
            cx, cy, orientation, tx, ty = self.get_table_centres(id, pos)
            sx = cx
            sy = cy
            ix = round(sx / reso)
            iy = round(sy / reso)
            gx = goals[id][0]
            gy = goals[id][1]

            # distance to goal
            d = np.hypot(sx - gx, sy - gy)
            if d >= reso:
                # ox and oy represent static obstacles
                # tx and ty represent the centre coordinates of the tables (dynamic)
                otx = self.ox + tx
                oty = self.oy + ty
                minix, miniy = self.next_cell(ix, iy, gx, gy, otx, oty, reso, rr)
                xp = minix * reso
                yp = miniy * reso
                # move table with id
                self.update_table(id, xp, yp, cx, cy, orientation)
                self.path.append((xp, yp))
            else:
                self.path.append((gx, gy))
                self.update_table(id, gx, gy, cx, cy, orientation)
                goals.pop(id) # remove entry from the goals as table is in the goal position


    def tables_to_goals(self, goals):

        # TO-DO: given a list of goal positions create a dictionary which maps a table to position
        # pos = self.camera.get_pos(self.number_of_tables)
        pos = self.tables
        tables_with_goals = dict()

        for id in pos:
            mindist = float("inf")
            optimal_goal = None
            # centre = [x, y]
            centre = (pos[id][0] + pos[id][2]) / 2
            for goal in goals:
                dist = np.hypot(goal[0] - centre[0], goal[1] - centre[1])
                if mindist >= dist:
                    mindist = dist
                    optimal_goal = goal
            tables_with_goals[id] = optimal_goal
            goals.remove(goal)

        while bool(tables_with_goals):
            self.multi_path(tables_with_goals)
        print("Goal!")

    def get_static_obstacles(self, obstacles):

        ox = []
        oy = []
        orad = []

        for id in obstacles:

            centre = (obstacles[id][0] + obstacles[id][1]) / 2
            ox.append(centre[0])
            oy.append(centre[1])
            r = np.hypot(centre[0] - obstacles[id][0][0], centre[1] - obstacles[id][0][1])
            orad.append(r)

        return ox, oy, orad

    #test data
    def set_table_centres(self):

        ar_diagonal = sqrt(19 * 19 * 2)
        radius = round(ar_diagonal / 2)

        # ar tag for table 1
        table1_id = 1
        center1 = (200, 230)
        rotation = pi / 6
        tag1 = Polygon(center1, radius, rotation, n=4)
        vertices = tag1.vertices
        p1 = np.array([vertices[3][0], vertices[3][1]], dtype=float)
        p2 = np.array([vertices[0][0], vertices[0][1]], dtype=float)
        p3 = np.array([vertices[1][0], vertices[1][1]], dtype=float)
        p4 = np.array([vertices[2][0], vertices[2][1]], dtype=float)
        ar1_coords = np.array([p1, p2, p3, p4])

        tables = {table1_id: ar1_coords}

        return tables

    def update_table(self, id, x, y, cx, cy, orientation):

        ar_diagonal = sqrt(19 * 19 * 2)
        radius = round(ar_diagonal / 2)

        target_orientation = np.array((x - cx, y - cy))

        rotation = self.angleBetweenVectors(orientation, target_orientation)
        ar_tag = Polygon(cx, cy, radius, rotation, n=4)
        vertices = ar_tag.vertices
        p1 = np.array([vertices[3][0], vertices[3][1]], dtype=float)
        p2 = np.array([vertices[0][0], vertices[0][1]], dtype=float)
        p3 = np.array([vertices[1][0], vertices[1][1]], dtype=float)
        p4 = np.array([vertices[2][0], vertices[2][1]], dtype=float)
        ar_coords = np.array([p1, p2, p3, p4])

        self.tables[id] = ar_coords

    def angleBetweenVectors(v1, v2) -> float:
        cos_a = np.dot(v1, v2)
        sin_a = la.norm(np.cross(v1, v2))
        return np.arctan2(sin_a, cos_a)

    def set_static_obstacles(self):

        p1 = np.array([333, 400])
        p2 = np.array([400, 466])
        coords1 = np.array([p1, p2])
        p1 = np.array([400, 300])
        p2 = np.array([450, 360])
        coords2 = np.array([p1, p2])
        p1 = np.array([500, 200])
        p2 = np.array([600, 250])
        coords3 = np.array([p1, p2])

        obstacles = {1: coords1, 2: coords2, 3: coords3}

        return obstacles

    def set_goal_cords(self):

        goal1 = (1235, 563)  # (x, y)
        return [goal1]
        # p = (525, 564)  #left
        # p = (936, 296)  #top
        # p = (1337, 551)  #right occupied now
        # p = (977, 920)  # bottom

    # def draw(self):
if __name__ == '__main__':
    Planner(1590, 1072)