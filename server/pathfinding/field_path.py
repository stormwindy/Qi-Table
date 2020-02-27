
import numpy as np
import numpy.linalg as la
from math import *
import sys
sys.path.append("..\\..\\")
from server.vision.camera import Camera
from server.vision.room import Room
from sympy import Polygon, Point2D
import matplotlib.pyplot as plt

class FieldPlanner:

    KP = 5
    ETA = 100000000

    def __init__(self, room_width, room_height, obstacles, grid_size, robot_radius):
        # self.number_of_tables = None
        # self.camera = Camera(0)
        self.room_width = room_width
        self.room_height = room_height
        self.grid_size = grid_size
        self.robot_radius = robot_radius
        # self.path = []
        self.goals = dict()
        self.tables = dict()
        self.paths = dict()
        # self.xs = []
        # self.ys = []
        self.ox, self.oy, self.orad = self.get_static_obstacles(obstacles)
        # self.ox, self.oy, self.orad = self.get_static_obstacles(Room(0).obsts)
        # self.ox, self.oy, self.orad = self.get_static_obstacles(self.set_static_obstacles())
        # self.plan()


    def get_table_centres(self, table_id, pos):

        """
        get_table_centres: returns centre coordinates and the orientation of the specified table,
        and the list of other table centres excluding one that was specified

        :param table_id : id of the table that should not be included in the list
        :param pos: dictionary of table id's & ar tag positions
        """

        # lists of dynamic obstacles (other tables)
        tx = []
        ty = []
        for id in pos:
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

    def calc_repulsive_potential(self, x, y, tx, ty):

        safe_radius = self.robot_radius

        # search nearest dynamic obstacle
        minid_d = -1
        dmin_d = float("inf")
        for i, _ in enumerate(tx):
            d = np.hypot(x - tx[i], y - ty[i])
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
            dq = np.hypot(x - tx[minid_d], y - ty[minid_d])
            # safe distance between tables (distance between tables is the distance btw their centres)
            safe_radius = self.robot_radius * 2
        # static obstacle is closer
        else:
            # calc repulsive potential
            dq = np.hypot(x - self.ox[minid_s], y - self.oy[minid_s])
            # safe distance = obstacle radius + robot radius
            safe_radius = self.orad[minid_s] + self.robot_radius

        if dq <= (safe_radius):
            if dq <= 0.1:
                dq = 0.1
            return 0.5 * self.ETA * (1.0 / dq - 1.0 / safe_radius) ** 2
        else:
            return 0.0

    def next_cell(self, cell_x, cell_y, gx, gy, ox, oy):

        """
        next_cell: returns next cell which minimizes the potential

        :param cell_x, cell_y: current cell coordinates
        :param gx, gy: goal coordinates
        :param ox, oy: lists of dynamic obstacle coordinates
        """

        # room boundaries in terms of grid coordinates
        # table centre position can't come closer to the wall than its radius
        grid_bound_left = int(round(self.robot_radius / self.grid_size))  # number of cells the radius takes
        grid_bound_right = int(round(self.room_width / self.grid_size - self.robot_radius / self.grid_size))
        grid_bound_top = int(round(self.robot_radius / self.grid_size))
        grid_bound_bottom = int(round(self.room_height / self.grid_size - self.robot_radius / self.grid_size))

        minix, miniy = -1, -1
        minuf = float("inf")
        # check all 8 cells around the table centre
        for ix in range((cell_x - 1), (cell_x + 2)):
            x = ix * self.grid_size
            for iy in range((cell_y - 1), (cell_y + 2)):
                y = iy * self.grid_size
                # the current cell should not be considered as it would result in robot staying in place
                # however might be useful for dynamic obstacle avoidance
                if ix == cell_x and iy == cell_y:
                    continue
                if ix <= grid_bound_right and ix >= grid_bound_left \
                        and iy <= grid_bound_bottom and iy >= grid_bound_top:
                    ug = self.calc_attractive_potential(x, y, gx, gy)
                    uo = self.calc_repulsive_potential(x, y, ox, oy)
                    uf = ug + uo
                else:
                    uf = float("inf")
                # find the cell that minimizes potential
                if minuf > uf:
                    minuf = uf
                    minix = ix
                    miniy = iy

        return minix, miniy


    def multi_path(self):

        """
        multi_path: computes the next step for each table and moves it

        """

        # goals = dictionary which maps table id with its goal

        # pos = self.camera.get_pos(self.number_of_tables)
        pos = self.tables
        # iterate through tables
        for id in pos:
            cx, cy, orientation, tx, ty = self.get_table_centres(id, pos)
            sx = cx
            sy = cy
            ix = int(round(sx / self.grid_size))
            iy = int(round(sy / self.grid_size))
            gx = self.goals[id][0]
            gy = self.goals[id][1]

            # distance to goal
            d = np.hypot(sx - gx, sy - gy)
            # if robot is not in the same grid as its goal position, find the optimal gird cell
            if d >= self.grid_size:
                # ox and oy represent static obstacles are attributes of the class (self.ox, self.oy)
                # tx and ty represent the centre coordinates of the tables (dynamic)
                minix, miniy = self.next_cell(ix, iy, gx, gy, tx, ty)
                xp = minix * self.grid_size
                yp = miniy * self.grid_size
                # move table with id
                self.update_table(id, xp, yp, cx, cy, orientation)
                self.paths[id][0].append(xp)
                self.paths[id][1].append(yp)
            # robot is in the same grid as its goal position, move it to its exact goal position
            else:
                self.paths[id][0].append(gx)
                self.paths[id][1].append(gy)
                self.update_table(id, gx, gy, cx, cy, orientation)
                # remove entry from the goals as table is in the goal position
                self.goals.pop(id)


    def tables_to_goals(self, goals):

        """
        tables_to_goals: returns a dictionary of table id to goal assignments

        NOTE: at the moment table is assigned to a goal that is closest to it using euclidean distance.
        Such assignment does not consider any obstacles and might not be optimal.
        Once the goal has been assigned to a table, it is removed from the list of goals, so no two tables will
        have the same goal.

        :param goals: list of goal positions

        """

        # pos = self.camera.get_pos(self.number_of_tables)
        pos = self.tables
        tables_with_goals = dict()

        # iterate through tables
        for id in pos:
            mindist = float("inf")
            optimal_goal = None
            # centre = [x, y]
            centre = (pos[id][0] + pos[id][2]) / 2
            for goal in goals:
                dist = np.hypot(goal[0] - centre[0], goal[1] - centre[1])
                # minimize the distance
                if mindist >= dist:
                    mindist = dist
                    optimal_goal = goal
            # assign goal to the table id
            tables_with_goals[id] = optimal_goal
            goals.remove(goal)

        return tables_with_goals

    def plan(self, goals):

        """
        plan: returns path for every table

        :param goals: list of goal positions

        """

        self.goals = self.tables_to_goals(goals)
        # while there are tables that are not at their goal positions
        while bool(self.goals):
            self.multi_path()
        return self.paths
        print("Goal!")

    def get_static_obstacles(self, obstacles):

        """
        get_static_obstacles: returns the centre coordinates and the radius for all static obstacles

        :param obstacles: dictionary of obstacles

        """

        ox = []
        oy = []
        orad = []

        for id in obstacles:

            # centre coordinates
            x = (obstacles[id][0][0] + obstacles[id][1][0]) / 2
            y = (obstacles[id][0][1] + obstacles[id][1][1]) / 2
            ox.append(x)
            oy.append(y)
            r = np.hypot(x - obstacles[id][0][0], y - obstacles[id][0][1])
            orad.append(r)

        return ox, oy, orad

# these are functions I have used for testing, most of them irrelevant to you

    # creates a dictionary tables manually instead of using a camera
    def set_table_centres(self, centres):


        ar_diagonal = sqrt(19 * 19 * 2)
        radius = round(ar_diagonal / 2)

        table_id = 1
        for c in centres:
            cx, cy = c
            rotation = pi / 6
            tag1 = Polygon(c, radius, rotation, n=4)
            vertices = tag1.vertices
            vertices = self.order_coords(vertices)
            p1 = np.array([vertices[0][0], vertices[0][1]], dtype=float)
            p2 = np.array([vertices[1][0], vertices[1][1]], dtype=float)
            p3 = np.array([vertices[2][0], vertices[2][1]], dtype=float)
            p4 = np.array([vertices[3][0], vertices[3][1]], dtype=float)
            ar_coords = np.array([p1, p2, p3, p4])

            # add initial coordinates to the path
            self.paths[table_id] = [[cx], [cy]]

            self.tables[table_id] = ar_coords

            table_id += 1

        return self.tables

    def order_coords(self, coords):

        ordered_coords = []
        miny = float("inf")
        first = -1
        for i in range(len(coords)):
            x = coords[i][0]
            y = coords[i][1]
            if y < miny:
                y = miny
                first = i
            if y == miny:
                if x < coords[first][0]:
                    first = i
                    break
        second = (first + 1) % 4
        third = (first + 2) % 4
        fourth = (first + 3) % 4
        ordered_coords = [coords[first], coords[second], coords[third], coords[fourth]]

        return ordered_coords

    def update_table(self, id, x, y, cx, cy, orientation):

        ar_diagonal = sqrt(19 * 19 * 2)
        radius = round(ar_diagonal / 2)

        target_orientation = np.array((x - cx, y - cy))

        rotation = self.angleBetweenVectors(orientation, target_orientation)
        ar_tag = Polygon((x, y), radius, rotation, n=4)
        vertices = ar_tag.vertices
        vertices = self.order_coords(vertices)
        p1 = np.array([vertices[0][0], vertices[0][1]], dtype=float)
        p2 = np.array([vertices[1][0], vertices[1][1]], dtype=float)
        p3 = np.array([vertices[2][0], vertices[2][1]], dtype=float)
        p4 = np.array([vertices[3][0], vertices[3][1]], dtype=float)
        ar_coords = np.array([p1, p2, p3, p4])

        self.tables[id] = ar_coords

    def angleBetweenVectors(self, v1, v2) -> float:
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

    def set_goal_coords(self):

        goal1 = (1235, 563)  # (x, y)
        return [goal1]

if __name__ == '__main__':
    