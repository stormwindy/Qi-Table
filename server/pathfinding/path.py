#! /usr/bin/env python

import numpy as np
import numpy.linalg as la
import sys
from math import floor, ceil
# from pathfinding.core.grid import Grid
from sympy import Polygon

sys.path.append('..\\..\\')
from base import *


class Path:
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
    goal_orientation = None
    # goal_center_pos = table_center(goal_ar1, goal_ar2)

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

    # number_of_cells_x = floor(room_width / table_width)
    # number_of_cells_y = floor(room_height / table_height)
    # number_of_cells = math.max(number_of_cells_x, number_of_cells_y)

    # TO DO
    # fix this as the number of cells along the width of the room and the height of the room must differ
    # if we want to achieve square grid cells
    cell_size = 1  # cell size = 1cm
    grid_matrix = np.zeros([ceil(room_width / cell_size), ceil(room_height / cell_size)])
    # grid = Grid(grid_matrix)

    # type vector
    Vector = np.array([])

    # def __init__(self):
    #     pass

    def vectorFromPoints(self, point1: Point2, point2: Point2) -> Vector:

        x1 = point1.x
        y1 = point1.y
        x2 = point1.x
        y2 = point2.y
        return np.array([x2 - x1, y2 - y1])

    def angleBetweenVectors(self, v1, v2) -> float:

        cos_a = np.dot(v1, v2)
        sin_a = la.norm(np.cross(v1, v2))
        return np.arctan2(sin_a, cos_a)

    def angleToHorizontal(self, point1: Point2, point2: Point2) -> float:

        horizontal_vector = self.vectorFromPoints(self.x_axis1, self.x_axis2)
        v = self.vectorFromPoints(point1, point2)
        return self.angleBetweenVectors(horizontal_vector, v)

    def angleToVertical(self, point1: Point2, point2: Point2) -> float:

        vertical_vector = self.vectorFromPoints(self.y_axis1, self.y_axis2)
        v = self.vectorFromPoints(point1, point2)
        return self.angleBetweenVectors(vertical_vector, v)

    # TO DO:
    # def updateGrid(self, table: Table) -> None:

    def updateGrid(self, left1: Point2, left2: Point2, right1: Point2, right2: Point2) -> None:

        self.grid_matrix.fill(0)

        table_pol = Polygon((left1.x, left1.y), (right1.x, right1.y), (right2.x, right2.y), (left2.x, left2.y))

        left1_cell = self.gridPosition(left1)
        left2_cell = self.gridPosition(left2)
        right1_cell = self.gridPosition(right1)
        right2_cell = self.gridPosition(right2)

        # rectangle formed from grid cells which encloses the shape of the table
        left_top = (left1_cell[0] * self.cell_size, left1_cell[1] * self.cell_size)
        left_bottom = (left1_cell[0] * self.cell_size, (left1_cell[1] + 1) * self.cell_size)
        right_bottom = ((right1_cell[0] + 1) * self.cell_size, (right2_cell[1] + 1) * self.cell_size)
        right_top = ((right2_cell[0] + 1) * self.cell_size, right1_cell[1] * self.cell_size)

        current_pos = left_top
        current_cell = left1_cell
        print(current_cell)
        count = 0

        while current_pos[1] <= right_bottom[1]:
            while current_pos[0] <= right_top[0]:
                print(current_cell)
                if table_pol.encloses_point(current_pos):

                    i = current_cell[0]
                    j = current_cell[1]
                    self.grid_matrix[i][j] = 1
                current_cell = (current_cell[0] + 1, current_cell[1])
                i = current_pos[0] + self.cell_size
                j = current_pos[1]
                current_pos = (i, j)
            count = count + 1
            current_pos = (left_top[0], current_pos[1] + self.cell_size)
            current_cell = (left1_cell[0] + count, left1_cell[1] + count)

        print(self.grid_matrix)

    Cell = np.array([])

    def gridPosition(self, point: Point2) -> Cell:
        """
        gridPosition: Compute in which grid the given point is

        :param point:
        :type point: Point2
        :rtype: Cell
        """

        cell_x = floor(point.x / self.cell_size) - 1
        cell_y = floor(point.y / self.cell_size) - 1
        return np.array([cell_x, cell_y])

    def table_centre(self, ar1: Point2, ar2: Point2) -> Point2:

        x = (ar1.x + ar2.x) / 2
        y = (ar1.y + ar2.y) / 2
        table_centre_pos = Point2(x, y)
        return table_centre_pos

if __name__ == "__main__":
    p1 = Point2(2, 2)
    p2 = Point2(2, 5)
    p3 = Point2(7, 2)
    p4 = Point2(7, 5)

    p = Path()
    p.updateGrid(p1, p2, p3, p4)
