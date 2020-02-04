# -*- coding: utf-8 -*-
from .node import Node
try:
    import numpy as np
    USE_NUMPY = True
except ImportError:
    USE_NUMPY = False
from .diagonal_movement import DiagonalMovement
import sys
sys.path.append('..\\..\\') #this is for windows
from table_functions import table_to_grid, table_occupied_cells
# sys.path.append('..//..//..//..//') #this is for linux/iOS
from base import *


def build_nodes(width, height, matrix=None, inverse=False):
    """
    create nodes according to grid size. If a matrix is given it
    will be used to determine what nodes are walkable.
    :rtype : list
    """
    nodes = []
    use_matrix = (isinstance(matrix, (tuple, list))) or \
        (USE_NUMPY and isinstance(matrix, np.ndarray) and matrix.size > 0)

    # NEW: sets itself variable to True if the the matrix entry is -1
    # walkable is still False in this case
    for y in range(height):
        nodes.append([])
        for x in range(width):
            # 1, '1', True will be walkable
            # while others will be obstacles
            # if inverse is False, otherwise
            # it changes
            weight = int(matrix[y][x]) if use_matrix else 1
            walkable = weight <= 0 if inverse else weight >= 1
            itself = weight == -1

            nodes[y].append(Node(x=x, y=y, walkable=walkable, weight=weight, itself=itself))
    return nodes


class Grid(object):
    def __init__(self, width=0, height=0, matrix=None, inverse=False):
        """
        a grid represents the map (as 2d-list of nodes).
        """
        self.width = width
        self.height = height
        if isinstance(matrix, (tuple, list)) or (
                USE_NUMPY and isinstance(matrix, np.ndarray) and
                matrix.size > 0):
            self.height = len(matrix)
            self.width = self.width = len(matrix[0]) if self.height > 0 else 0
        if self.width > 0 and self.height > 0:
            self.nodes = build_nodes(self.width, self.height, matrix, inverse)
        else:
            self.nodes = [[]]

    def node(self, x, y):
        """
        get node at position
        :param x: x pos
        :param y: y pos
        :return:
        """
        return self.nodes[y][x]

    def inside(self, x, y):
        """
        check, if field position is inside map
        :param x: x pos
        :param y: y pos
        :return:
        """
        return 0 <= x < self.width and 0 <= y < self.height

    # NEW returns if the node has itself value set to True
    def itself(self, x, y):

        return self.nodes[y][x].itself

    def walkable(self, x, y):
        """
        check, if the tile is inside grid and if it is set as walkable
        """
        return self.inside(x, y) and self.nodes[y][x].walkable

    def neighbors(self, node, diagonal_movement=DiagonalMovement.never):
        """
        get all neighbors of one node
        :param node: node
        """
        x = node.x
        y = node.y
        neighbors = []
        s0 = d0 = s1 = d1 = s2 = d2 = s3 = d3 = False

        # NEW: modified so that if the neighboring cell is not walkable
        # then check if it is the table itself, continues to check towards
        # desired direction until finds the cell outside the bounds of table
        # if it is walkable adds the table center's neighbor to the list
        # ↑
        if self.walkable(x, y - 1):
            neighbors.append(self.nodes[y - 1][x])
            s0 = True
        elif self.itself(x, y - 1):
            y_up = y - 2
            while self.inside(x, y_up) and self.itself(x, y_up):
                y_up = y_up - 1
            if self.walkable(x, y_up):
                neighbors.append(self.nodes[y - 1][x])
                s0 = True

        # →
        if self.walkable(x + 1, y):
            neighbors.append(self.nodes[y][x + 1])
            s1 = True
        elif self.itself(x + 1, y):
            x_right = x + 2
            while self.inside(x_right, y) and self.itself(x_right, y):
                x_right = x_right + 1
            if self.walkable(x_right, y):
                neighbors.append(self.nodes[y][x + 1])
                s1 = True
        # ↓
        if self.walkable(x, y + 1):
            neighbors.append(self.nodes[y + 1][x])
            s2 = True
        elif self.itself(x, y + 1):
            y_down = y + 2
            while self.inside(x, y_down) and self.itself(x, y_down):
                y_down = y_down + 1
            if self.walkable(x, y_down):
                neighbors.append(self.nodes[y + 1][x])
                s2 = True

        # ←
        if self.walkable(x - 1, y):
            neighbors.append(self.nodes[y][x - 1])
            s3 = True
        elif self.itself(x + 1, y):
            x_left = x - 2
            while self.inside(x_left, y) and self.itself(x_left, y):
                x_left = x_left - 1
            if self.walkable(x_left, y):
                neighbors.append(self.nodes[y][x - 1])
                s3 = True

        if diagonal_movement == DiagonalMovement.never:
            return neighbors

        if diagonal_movement == DiagonalMovement.only_when_no_obstacle:
            d0 = s3 and s0
            d1 = s0 and s1
            d2 = s1 and s2
            d3 = s2 and s3
        elif diagonal_movement == DiagonalMovement.if_at_most_one_obstacle:
            d0 = s3 or s0
            d1 = s0 or s1
            d2 = s1 or s2
            d3 = s2 or s3
        elif diagonal_movement == DiagonalMovement.always:
            d0 = d1 = d2 = d3 = True

        # ↖
        if d0 and self.walkable(x - 1, y - 1):
            neighbors.append(self.nodes[y - 1][x - 1])
        elif self.itself(x - 1, y - 1):
            x_left = x - 2
            y_up = y - 2
            while self.inside(x_left, y_up) and self.itself(x_left, y_up):
                x_left = x_left - 1
                y_up = y_up - 1
            if self.walkable(x_left, y_up):
                neighbors.append(self.nodes[y - 1][x - 1])

        # ↗
        if d1 and self.walkable(x + 1, y - 1):
            neighbors.append(self.nodes[y - 1][x + 1])
        elif self.itself(x + 1, y - 1):
            x_right = x + 2
            y_up = y - 2
            while self.inside(x_right, y_up) and self.itself(x_right, y_up):
                x_right = x_right - 1
                y_up = y_up - 1
            if self.walkable(x_right, y_up):
                neighbors.append(self.nodes[y - 1][x + 1])

        # ↘
        if d2 and self.walkable(x + 1, y + 1):
            neighbors.append(self.nodes[y + 1][x + 1])
        elif self.itself(x + 1, y + 1):
            x_right = x + 2
            y_down = y + 2
            while self.inside(x_right, y_down) and self.itself(x_right, y_down):
                x_right = x_right + 1
                y_down = y_down + 1
            if self.walkable(x_right, y_down):
                neighbors.append(self.nodes[y + 1][x + 1])

        # ↙
        if d3 and self.walkable(x - 1, y + 1):
            neighbors.append(self.nodes[y + 1][x - 1])
        elif self.itself(x - 1, y + 1):
            x_left = x - 2
            y_down = y + 2
            while self.inside(x_left, y_down) and self.itself(x_left, y_down):
                x_left = x_left - 1
                y_down = y_down + 1
            if self.walkable(x_left, y_down):
                neighbors.append(self.nodes[y + 1][x - 1])

        return neighbors

    # NEW: given the table iterates the list of neighbors to find if the
    # table center could be moved to that position
    def filter_with_safe_dist(self, neighbors, table):

        for i in neighbors:
            next_node = i
            x_next = next_node.x
            y_next = next_node.y
            rectangle = table.geometry
            rectangle.central_position = Point2(x_next, y_next)
            # TO DO: table corner coordinates need to be moved with respect to its new center position
            rectangle.left1 = Point2(0, 0)
            rectangle.left2 = Point2(0, 0)
            rectangle.right1 = Point2(0, 0)
            rectangle.right2 = Point2(0, 0)
            next_table = table
            table.geometry = rectangle
            table.table_id = -1
            new_grid = table_to_grid(next_table, False)
            possible = False
            occupied = table_occupied_cells(next_table)
            for j in occupied:
                # might be other way around
                possible = possible or new_grid[j[1]][j[0]] == 1
                if possible:
                    break
            if possible:
                neighbors.remove(i)


    def cleanup(self):
        for y_nodes in self.nodes:
            for node in y_nodes:
                node.cleanup()

    def grid_str(self, path=None, start=None, end=None,
                 border=True, start_chr='s', end_chr='e',
                 path_chr='x', empty_chr=' ', block_chr='#',
                 show_weight=False):
        """
        create a printable string from the grid using ASCII characters

        :param path: list of nodes that show the path
        :param start: start node
        :param end: end node
        :param border: create a border around the grid
        :param start_chr: character for the start (default "s")
        :param end_chr: character for the destination (default "e")
        :param path_chr: character to show the path (default "x")
        :param empty_chr: character for empty fields (default " ")
        :param block_chr: character for blocking elements (default "#")
        :param show_weight: instead of empty_chr show the cost of each empty
                            field (shows a + if the value of weight is > 10)
        :return:
        """
        data = ''
        if border:
            data = '+{}+'.format('-'*len(self.nodes[0]))
        for y in range(len(self.nodes)):
            line = ''
            for x in range(len(self.nodes[y])):
                node = self.nodes[y][x]
                if node == start:
                    line += start_chr
                elif node == end:
                    line += end_chr
                elif path and ((node.x, node.y) in path or node in path):
                    line += path_chr
                elif node.walkable:
                    # empty field
                    weight = str(node.weight) if node.weight < 10 else '+'
                    line += weight if show_weight else empty_chr
                else:
                    line += block_chr  # blocked field
            if border:
                line = '|'+line+'|'
            if data:
                data += '\n'
            data += line
        if border:
            data += '\n+{}+'.format('-'*len(self.nodes[0]))
        return data

if __name__ == "__main__":
    pass