#! /usr/bin/env python

import numpy as np
import numpy.linalg as la
import sys
from math import floor, ceil
from pathfinding_lib.core.diagonal_movement import DiagonalMovement
from pathfinding_lib.core.grid import Grid
from pathfinding_lib.finder.a_star import AStarFinder
from sympy import Polygon
from table_functions import table_to_grid, grid_position

sys.path.append('..\\..\\') #this is for windows
# sys.path.append('..//..//') #this is for linux/iOS
from base import *

class Path_Smilte:

    # maps table to its desired position
    tables_goals = dict()

    tables = []

    p1 = Point2(3, 3)
    p2 = Point2(3, 6)
    p3 = Point2(8, 3)
    p4 = Point2(8, 6)
    pc = Point2(5.5, 4.5)
    rectangle = Rectangle(5, 3, pc, 0, p1, p2, p3, p4)
    table1 = Table(rectangle, 1)

    p1 = Point2(16, 5)
    p2 = Point2(16, 6)
    p3 = Point2(17, 5)
    p4 = Point2(17, 6)
    pc = Point2(16.5, 5.5)
    rectangle = Rectangle(1, 1, pc, 0, p1, p2, p3, p4)
    table2 = Table(rectangle, 2)

    p1 = Point2(14, 7)
    p2 = Point2(14, 9)
    p3 = Point2(17, 7)
    p4 = Point2(17, 9)
    pc = Point2(15.5, 8)
    rectangle = Rectangle(5, 3, pc, 0, p1, p2, p3, p4)
    table3 = Table(rectangle, 3)

    tables = [table1, table2, table3]

    goal_position_center = Point2(15.5, 2)

    room_width = 25
    room_height = 15

    # TO DO:
    initial_orientation = None
    goal_orientations = None # dictionary which maps table id to its goal position
    # goal_center_pos = table_center(goal_ar1, goal_ar2)

    number_of_tables = None

    # TO DO
    # fix this as the number of cells along the width of the room and the height of the room must differ
    # if we want to achieve square grid cells
    cell_size = 1  # cell size = 1cm
    grid_matrix = np.empty([ceil(room_height / cell_size), ceil(room_width / cell_size)])

    # Updates the grid so all the tables are represented in respect to the table which table_id is given
    def update_grid(self, table_id) -> None:

        # c = Camera(1)
        # pos = c.get_pos(2) where 2 is the number of tables in the room
        # print(pos) e.g. {3: ((555, 674), (999, 611)), 1: ((397, 861), (163, 484))}
        # c.release()

        self.grid_matrix.fill(1)
        # print(self.grid_matrix)
        for i in self.tables:
            table = i
            if table.table_id == table_id:
                self.grid_matrix = table_to_grid(table, True, self.grid_matrix)
            else:
                self.grid_matrix = table_to_grid(table, False, self.grid_matrix)


    def find(self, table: Table, goal_pos: Point2):

        self.update_grid(table.table_id)
        grid = Grid(matrix=self.grid_matrix)

        initial_pos = table.geometry.central_position
        # goal_pos = Point2(8, 8)
        initial_cell = grid_position(initial_pos)
        start = grid.node(initial_cell[1], initial_cell[0])
        goal_cell = grid_position(goal_pos)
        goal = grid.node(goal_cell[1], goal_cell[0])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(table, start, goal, grid)
        #path is list of tuples starting from initial position (-1) and ending in goal position (-1)
        print(path)
        print(runs)
        print(grid.grid_str(path=path, start=start, end=goal))

    def assign_goal(self, table, goal_positions) -> None:
        pass




if __name__ == "__main__":

    p = Path_Smilte()
    p.find(p.table3, p.goal_position_center)
