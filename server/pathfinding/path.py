#! /usr/bin/env python

import numpy as np
import math
from pathfinding.core.grid import Grid
from base import Point2
from sympy import Line

class Path:

    # get from the vision
    initial_top_left_corner = Point2(0, 20)
    initial_bottom_left_corner = Point2(0, 0)
    initial_top_right_corner = Point2(30, 20)
    initial_bottom_right_corner = Point2(30, 0)

    # get from the app??
    goal_top_left_corner = Point2(70, 90)
    goal_bottom_left_corner = Point2()
    goal_right_corner = Point2(4, 4)

    initial_center_pos = Point2(1, 1)
    goal_center_pos = Point2(4, 6)
    distance = initial_center_pos.distanceTo(goal_center_pos)

    table_width = 30
    table_height = 20
    room_width = 100
    room_height = 150

    # x_axis_left = Point2(0, 0)
    # x_axis_right = Point2(room_width, 0)
    # y_axis_left = Point2(0, room_height)
    # y_axis_right = Point2(room_width, room_height)

    x_normal =
    y_normal =

    # number_of_cells_x = math.floor(room_width / table_width)
    # number_of_cells_y = math.floor(room_height / table_height)
    # number_of_cells = math.max(number_of_cells_x, number_of_cells_y)
    number_of_cells = 50
    grid = Grid(np.zeros(number_of_cells, number_of_cells, number_of_cells))

    def gridPosition(self, point: Point2):
        """
        gridPosition: Compute in which grid the given point is

        :param point:
        :type point: Point2
        :rtype: array
        """
        cell_size = self.room_width / self.number_of_cells
        cell_x = math.floor(point.get_x / cell_size) - 1
        cell_y = math.floor(point.get_y / cell_size) - 1
        return np.array([cell_x, cell_y])

    pass

