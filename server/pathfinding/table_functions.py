#! /usr/bin/env python

from math import floor, degrees
from typing import List

from sympy import Polygon
import numpy as np
import numpy.linalg as la
import sys

sys.path.append("..\\..\\")
from base import Table, Point2

# maps table id with the list of tuples representing the grid cells that the table occupies
occupied_cells = dict()

room_width = 25
room_height = 15
cell_size = 1

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

# type vector
Vector = np.array([])


def vectorFromPoints(point1: Point2, point2: Point2) -> Vector:
    x1 = point1.x
    y1 = point1.y
    x2 = point2.x
    y2 = point2.y
    return np.array([x2 - x1, y2 - y1])


def angleBetweenVectors(v1, v2) -> float:
    cos_a = np.dot(v1, v2)
    sin_a = la.norm(np.cross(v1, v2))
    return degrees(np.arctan2(sin_a, cos_a))


def angleToHorizontal(point1: Point2, point2: Point2) -> float:
    horizontal_vector = vectorFromPoints(x_axis1, x_axis2)
    v = vectorFromPoints(point1, point2)
    return angleBetweenVectors(horizontal_vector, v)


def angleToVertical(point1: Point2, point2: Point2) -> float:
    vertical_vector = vectorFromPoints(y_axis1, y_axis2)
    v = vectorFromPoints(point1, point2)
    return angleBetweenVectors(vertical_vector, v)


# puts table on the grid, where:
# 1  -> unoccupied
# 0  -> occupied by another table or obstacle
# -1 -> table itself
def table_to_grid(table: Table, itself: bool, grid_matrix):
    p1 = table.geometry.left1
    p2 = table.geometry.left2
    p3 = table.geometry.right1
    p4 = table.geometry.right2

    table_pol = Polygon((p1.x, p1.y), (p3.x, p3.y), (p4.x, p4.y), (p2.x, p2.y))

    p1_cell = grid_position(p1)
    p2_cell = grid_position(p2)
    p3_cell = grid_position(p3)
    p4_cell = grid_position(p4)

    count = 0

    max_y = max([p1_cell[0], p2_cell[0], p3_cell[0], p4_cell[0]])
    max_x = max([p1_cell[1], p2_cell[1], p3_cell[1], p4_cell[1]])
    min_y = min([p1_cell[0], p2_cell[0], p3_cell[0], p4_cell[0]])
    min_x = min([p1_cell[1], p2_cell[1], p3_cell[1], p4_cell[1]])
    current_cell = (min_y, min_x)
    while current_cell[0] <= max_y:
        while current_cell[1] <= max_x:
            if table_pol.encloses_point((current_cell[1], current_cell[0] + 1)) \
                    or table_pol.encloses_point((current_cell[1] + 1, current_cell[0] + 1)) \
                    or table_pol.encloses_point((current_cell[1], current_cell[0])) \
                    or table_pol.encloses_point((current_cell[1] + 1, current_cell[0])):
                i = current_cell[0]
                j = current_cell[1]
                print(i, j)
                if itself:
                    grid_matrix[i][j] = -1
                else:
                    grid_matrix[i][j] = 0
                occupied_cells(table, i, j)
            current_cell = (current_cell[0], current_cell[1] + 1)
        count = count + 1
        current_cell = (min_y + count, min_x)

    # print(grid_matrix)
    return grid_matrix

# given the cell coordinates adds it and all surrounding cell coordinates to the dictionary
# of the cells that the table occupies
# this helps to establish the safe distance
def occupied_cells(table: Table, i: int, j: int):
    occupied_cells = [(i, j), (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1), (i + 1, j + 1), (i - 1, j - 1),
                            (i + 1, j - 1), (i - 1, j + 1)]
    occupied_cells = list(dict.fromkeys(occupied_cells))
    occupied_cells[table.table_id] = table_occupied_cells


def grid_position(point: Point2) -> tuple:
    """
    gridPosition: Compute in which grid the given point is

    :param point:
    :type point: Point2
    :rtype: tuple
    """

    cell_x = floor(point.x / cell_size)
    cell_y = floor(point.y / cell_size)
    # print((cell_y, cell_x))
    return (cell_y, cell_x)


def table_centre(ar1: Point2, ar2: Point2) -> Point2:
    x = (ar1.x + ar2.x) / 2
    y = (ar1.y + ar2.y) / 2
    table_centre_pos = Point2(x, y)
    return table_centre_pos


def table_occupied_cells(table: Table) -> List:
    return occupied_cells[table.table_id]
