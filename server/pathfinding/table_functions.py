#! /usr/bin/env python

from math import floor, degrees
from typing import List

from sympy import Polygon
import numpy as np
import numpy.linalg as la
import sys

sys.path.append("..\\..\\")
from base import Table, Point2, Rectangle

# maps table id with the list of tuples representing the grid cells that the table occupies
occupied_cells = dict()

room_width = 25
room_height = 15
cell_size = 1

# type vector
Vector = np.array([])


def vectorFromPoints(point1: Point2, point2: Point2) -> Vector:

    return np.array([point2.x - point1.x, point2.y - point1.y])


def angleBetweenVectors(v1, v2) -> float:
    cos_a = np.dot(v1, v2)
    sin_a = la.norm(np.cross(v1, v2))
    return degrees(np.arctan2(sin_a, cos_a))


def angleToHorizontal(point1: Point2, point2: Point2) -> float:
    x_axis1, x_axis2= Point2(0, 0), Point2(room_width, 0)
    horizontal_vector = vectorFromPoints(x_axis1, x_axis2)
    v = vectorFromPoints(point1, point2)
    return angleBetweenVectors(horizontal_vector, v)


def angleToVertical(point1: Point2, point2: Point2) -> float:
    y_axis1, y_axis2 = Point2(0, room_height), Point2(room_width, room_height)
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

    print("table id", table.table_id)
    print(p1.x, p2.x, p3.x, p4.x)

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

def form_table(ar1 : Point2, ar2 : Point2, table_id : int) -> Table:

    # to make sure the ar1 tag corresponds to the left and ar2 to the right
    #might not need this if the tags are always returned in a left to right manner
    if(ar1.x > ar2.x):
        t = ar1
        ar1 = ar2
        ar2 = t

    width = 2
    height = 2
    central_position = table_centre(ar1, ar2)
    if(ar1.y < ar2.y):
        orientation =  angleToHorizontal(ar1,ar2)
    elif(ar1.y >= ar2.y):
        orientation = -1 * angleToHorizontal(ar1,ar2)

    # orientation is positive if AR vector points towards bottom right
    # orientation is negative if AR vector points towards upper right
    # eg: orientation = -30 ; angle = 60
    #     orientation = 30 ; angle = 120
    angle = 90 + orientation
    print("orientation  = ", orientation)
    print("angle = ", angle)

    left1 = coordinate((180+angle), (width/2), ar1)
    right1 = coordinate((180+angle), (width / 2), ar2)
    left2 = coordinate(angle, (width/2), ar1)
    right2 = coordinate(angle, (width/2), ar2)

    geometry = Rectangle( width, height, central_position, orientation, left1, left2, right1, right2)

    table = Table(geometry,table_id)
    return table

def coordinate(theta: float, d: float, start_point: Point2) -> Point2:
    x = start_point.x + (d * np.cos(np.radians(theta)))

    y = start_point.y + (d * np.sin(np.radians(theta)))
    p = Point2(x, y)
    return p

def diagonal(table: Table) -> float:

    rectangle = table.geometry
    return rectangle.left1.distanceTo(rectangle.right2)