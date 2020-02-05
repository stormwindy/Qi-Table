#! /usr/bin/env python

import numpy as np
import numpy.linalg as la
import sys
from math import floor, ceil
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from sympy import Polygon

sys.path.append('..//..//')
from base import *


class Path_meg:
    # table initial coordinates
    # get from the vision & calculate another 2
    # initial_top_left_corner = Point2(0, 20)
    # initial_bottom_left_corner = Point2(0, 0)
    # initial_top_right_corner = Point2(30, 20)
    # initial_bottom_right_corner = Point2(30, 0)

    # get from the app??
    # goal_top_left_corner = Point2(70, 90)
    # goal_bottom_left_corner = Point2()
    # goal_top_right_corner = Point2()
    # goal_bottom_right_corner = Point2()

    table_width = 30
    table_height = 20
    room_width = 10
    room_height = 15

    # TO DO:
    initial_orientation = None
    goal_orientations = None # dictionary which maps table id to its goal position
    # goal_center_pos = table_center(goal_ar1, goal_ar2)


    number_of_tables = None

    # initial_center_pos = table_center(ar1, ar2)
    # distance = initial_center_pos.distanceTo(goal_center_pos)

    # initial_rectangle =  Rectangle(table_width, table_height, table_center(ar1, ar2), initial_orientation)
    # initial_table = Table(initial_rectangle)
    # goal_rectangle = Rectangle(table_width, table_height, goal_center_pos, goal_orientation)
    # goal_table = Table(goal_rectangle)

    x_axis_x1 = 0
    x_axis_y1 = 0
    x_axis_x2 = room_width
    x_axis_y2 = 0
    y_axis_x1 = 0
    y_axis_y1 = room_height
    y_axis_x2 = room_width
    y_axis_y2 = room_height

    x_axis1 = Point2(0, 0)
    x_axis2 = Point2(room_width, 0)
    y_axis1 = Point2(0, room_height)
    y_axis2 = Point2(room_width, room_height)

    # normals used to compute the angle between the side of the table and the norm
    # x_axis = Line((x_axis_x1, x_axis_y1), (x_axis_x2, x_axis_y2))
    # y_axis = Line((y_axis_x1, y_axis_y1), (y_axis_x2, y_axis_y2))

    # TO DO
    # fix this as the number of cells along the width of the room and the height of the room must differ
    # if we want to achieve square grid cells
    cell_size = 1  # cell size = 1cm
    grid_matrix = np.empty([ceil(room_width / cell_size), ceil(room_height / cell_size)])

    # type vector
    Vector = np.array([])

    def vectorFromPoints(self, point1: Point2, point2: Point2) -> Vector:

        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y
        return np.array([x2 - x1, y2 - y1])

    def angleBetweenVectors(self, v1, v2) -> float:

        cos_a = np.dot(v1, v2)
        sin_a = la.norm(np.cross(v1, v2))
        return math.degrees(np.arctan2(sin_a, cos_a))

    def angleToHorizontal(self, point1: Point2, point2: Point2) -> float:

        horizontal_vector = self.vectorFromPoints(self.x_axis1, self.x_axis2)
        v = self.vectorFromPoints(point1, point2)
        print(self.angleBetweenVectors(v,horizontal_vector))
        return self.angleBetweenVectors(v,horizontal_vector)

    def angleToVertical(self, point1: Point2, point2: Point2) -> float:

        vertical_vector = self.vectorFromPoints(self.y_axis1, self.y_axis2)
        v = self.vectorFromPoints(point1, point2)
        return self.angleBetweenVectors(vertical_vector, v)

    # TO DO:
    # def updateGrid(self, table: Table) -> None:

    def table_to_grid(self, p1: Point2, p2: Point2, p3: Point2, p4: Point2) -> None:

        # TO DO:
        # when we have multiple tables move this out of the function
        self.grid_matrix.fill(1)

        table_pol = Polygon((p1.x, p1.y), (p3.x, p3.y), (p4.x, p4.y), (p2.x, p2.y))

        p1_cell = self.grid_position(p1)
        p2_cell = self.grid_position(p2)
        p3_cell = self.grid_position(p3)
        p4_cell = self.grid_position(p4)

        count = 0

        max_y = max([p1_cell[0], p2_cell[0], p3_cell[0], p4_cell[0]])
        max_x = max([p1_cell[1], p2_cell[1], p3_cell[1], p4_cell[1]])
        min_y = min([p1_cell[0], p2_cell[0], p3_cell[0], p4_cell[0]])
        min_x = min([p1_cell[1], p2_cell[1], p3_cell[1], p4_cell[1]])
        current_cell = (min_y, min_x)
        while current_cell[0] <= max_y:
            while current_cell[1] <= max_x:
                # print(current_cell)
                if table_pol.encloses_point((current_cell[1], current_cell[0] + 1)) \
                        or table_pol.encloses_point((current_cell[1] + 1, current_cell[0] + 1)) \
                        or table_pol.encloses_point((current_cell[1], current_cell[0])) \
                        or table_pol.encloses_point((current_cell[1] + 1, current_cell[0])):
                    i = current_cell[0]
                    j = current_cell[1]
                    self.grid_matrix[i][j] = 0
                current_cell = (current_cell[0], current_cell[1] + 1)
            count = count + 1
            current_cell = (min_y + count, min_x)

        print(self.grid_matrix)

    def grid_position(self, point: Point2) -> tuple:
        """
        gridPosition: Compute in which grid the given point is

        :param point:
        :type point: Point2
        :rtype: tuple
        """

        cell_x = floor(point.x / self.cell_size)
        cell_y = floor(point.y / self.cell_size)
        # print((cell_y, cell_x))
        return (cell_y, cell_x)

    def table_centre(self, ar1: Point2, ar2: Point2) -> Point2:

        x = (ar1.x + ar2.x) / 2
        y = (ar1.y + ar2.y) / 2
        table_centre_pos = Point2(x, y)
        return table_centre_pos

    def update_grid(self) -> None:

        # c = Camera(1)
        # pos = c.get_pos(2) where 2 is the number of tables in the room
        # print(pos) e.g. {3: ((555, 674), (999, 611)), 1: ((397, 861), (163, 484))}
        # c.release()

        # TO DO
        #

        pass

    def coordinate(self, theta : float, d : float, start_point : Point2 ) -> Point2:
        x = start_point.x + (d* np.cos(np.radians(theta)))

        y = start_point.y + (d* np.sin(np.radians(theta)))
        p = Point2(x,y)
        return p

    def form_table(self, ar1 : Point2, ar2 : Point2, table_id : int) -> Table:
        p = Path_meg()
        # to make sure the ar1 tag corresponds to the left and ar2 to the right
        #might not need this if the tags are always returned in a left to right manner
        if(ar1.x > ar2.x):
            t = ar1
            ar1 = ar2
            ar2 = t

        width = 2
        height = 2
        central_position = p.table_centre(ar1, ar2)
        if(ar1.y < ar2.y):
            orientation =  p.angleToHorizontal(ar1,ar2)
        elif(ar1.y >= ar2.y):
            orientation = -1 * p.angleToHorizontal(ar1,ar2)

        # orientation is positive if AR vector points towards bottom right
        # orientation is negative if AR vector points towards upper right
        # eg: orientation = -30 ; angle = 60
        #     orientation = 30 ; angle = 120
        angle = 90 + orientation
        print("orientation  = ", orientation)
        print("angle = ", angle)

        left1 = p.coordinate((180+angle), (width/2), ar1)
        right1 = p.coordinate((180+angle), (width / 2), ar2)
        left2 = p.coordinate(angle, (width/2), ar1)
        right2 = p.coordinate(angle, (width/2), ar2)

        geometry = Rectangle( width, height, central_position, orientation, left1, left2, right1, right2)

        table = Table(geometry,table_id)
        return table


    def find(self):#, initial_pos: Point2, goal_pos: Point2):


        # c = Camera(1)
        # pos = c.get_pos(2) where 2 is the number of tables in the room
        # print(pos) e.g. {3: ((555, 674), (999, 611)), 1: ((397, 861), (163, 484))}
        # c.release()

        grid = Grid(matrix=self.grid_matrix)

        initial_pos = Point2(1, 1)
        goal_pos = Point2(8, 8)
        initial_cell = self.grid_position(initial_pos)
        start = grid.node(initial_cell[0], initial_cell[1])
        goal_cell = self.grid_position(goal_pos)
        goal = grid.node(goal_cell[0], goal_cell[1])


        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, goal, grid)
        #path is list of tuples starting from initial position (-1) and ending in goal position (-1)
        print(path)
        print(runs)
        print(grid.grid_str(path=path, start=start, end=goal))

    def assign_goal(self, Table, goal_positions) -> None:
        pass
    def get_table_attributes(selfself , table :Table):

        print(table.geometry.width)
        print(table.geometry.height)
        print(table.geometry.central_position.x , table.geometry.central_position.y)
        print(table.geometry.orientation)

        print(table.geometry.left1.x, table.geometry.left1.y)
        print(table.geometry.left2.x, table.geometry.left2.y)

        print(table.geometry.right1.x, table.geometry.right1.y)
        print(table.geometry.right2.x, table.geometry.right2.y)

        print(table.table_id)



if __name__ == "__main__":
    p1 = Point2(2, 2)
    p2 = Point2(7, 2)
    p3 = Point2(2, 5)
    p4 = Point2(7, 5)

    p = Path_meg()
    p.table_to_grid(p1, p2, p3, p4)
    a= p.vectorFromPoints(p1,p2)
    b=p.vectorFromPoints(p2, p4)
    c=p.vectorFromPoints(p2, p3)
    d=p.vectorFromPoints(p3, p2)
    print(a)
    print(b)
    print(c)
    print(d)
    # main 0 -->
    p.angleToHorizontal(p1,p2)
    # 180 <--
    p.angleToHorizontal(p2,p1)

    p.angleToHorizontal(p2, p4)
    p.angleToHorizontal(p4, p2)

    p.angleToHorizontal(p2, p3)
    # main - left to right up
    p.angleToHorizontal(p3, p2)
    #main - left ot right down
    p.angleToHorizontal(p1, p4)

    p.find()
    ar1 = Point2(1,1)
    ar2 = Point2(3,3)
    table = p.form_table(ar1,ar2, 1)



