#! /usr/bin/env python

import numpy as np
import math
import numpy.linalg as la
from pathfinding.core.grid import Grid
from base import *
from sympy import Polygon, Line

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
    room_width = 100
    room_height = 150

    # TO DO:
    initial_orientation = None
    goal_orientation = None
    goal_center_pos = table_center(goal_ar1, goal_ar2)

    # initial_center_pos = table_center(ar1, ar2)
    # distance = initial_center_pos.distanceTo(goal_center_pos)


    initial_rectangle =  Rectangle(table_width, table_height, table_center(ar1, ar2), initial_orientation)
    initial_table = Table(initial_rectangle)
    goal_rectangle = Rectangle(table_width, table_height, goal_center_pos, goal_orientation)
    goal_table = Table(goal_rectangle)

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

    # number_of_cells_x = math.floor(room_width / table_width)
    # number_of_cells_y = math.floor(room_height / table_height)
    # number_of_cells = math.max(number_of_cells_x, number_of_cells_y)
    number_of_cells = 50
    grid = Grid(np.zeros(number_of_cells, number_of_cells, number_of_cells))

    def vectorFromPoints(self, point1: Point2, point2: Point2):

        x1 = point1.get_x()
        y1 = point1.get_y()
        x2 = point1.get_x()
        y2 = point2.get_y()
        return np.array([x2-x1, y2-y1])

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

    def updateGrid(self, table: Table) -> None:

        pass


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


