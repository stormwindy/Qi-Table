#! /usr/bin/env python

import math
import numpy as np
from typing import List
from random import random, randint

class Point2:
    """
    Point2: Generic 2D point
    """
    x = None
    y = None

    def __init__(self, x: float, y: float) -> 'Point2':
        """
        Point2 constructor

        :param x: x position (in meters)
        :type x: float
        :param y: y position (in meters)
        :type y: float
        :rtype: Point2
        """
        self.x = x
        self.y = y

    def as_row_vec(self):
        """
        Return a copy of the vec as a row vector
        :return: numpy row vector
        """
        return np.array([[self.x,self.y]])

    def as_col_vec(self):
        """
        Return a copy of the vec as a column vector
        :return: numpy column vector
        """
        return np.array([[self.x,self.y]]).T

    def distanceTo(self, point: 'Point2') -> float:
        """
        distanceTo: Calculate the L2 norm from this point to another

        :param point: The other point
        :type point: Point2
        :rtype: float
        """
        return math.sqrt(
                math.pow( self.x - point.x, 2) +
                math.pow( self.y - point.y, 2)
        )


class Rectangle:
    """
    Rectangle: The base class for all rectangles (e.g. tables, obstacles, etc.)
    """
    width       = None
    height      = None
    position    = None
    orientation = None

    def __init__(self, width: float, height: float, position: Point2, orientation: float):
        """
        Constructor method for Rectangles.

        :param width: Width in meters
        :type width: float
        :param height: Height in meters.
        :type height: float
        :param position: 2D position of this table
        :type position: Point2
        :param orientation: Table orientation
        :type orientation: float
        """
        self.width    = width
        self.height   = height
        self.position = position
        self.orientation = orientation

    def intersects(self, rect: 'Rectangle') -> bool:
        """
        Helper function to determine if this rectangle intersects another (for
        pathfinding, etc.)

        :param rect: the other rectangle
        :type rect: Rectangle
        :return: true if intersecting
        :rtype: bool
        """
        # see https://stackoverflow.com/questions/10962379/how-to-check-intersection-between-2-rotated-rectangles
        raise NotImplementedError("TODO: implement polygon intersection")


class Table:
    """
    Base table class, including geometry information, world pos, device ID, etc.
    """
    geometry = None
    name     = None

    def __init__(self, geometry: Rectangle, name=None):
        """
        Initialize the table.

        :param geometry: Table geometry.
        :type geometry: Rectangle
        """
        self.geometry = geometry
        self.name = name
        if name is None:
            print('unnamed table created!')

class Layout:
    """
    Layout class, containing a mapping Table name -> Point2
    """
    mapping = {}

    def __init__(self, mapping={}):
        """
        Initialize the layout mapping, with an optional premade layout

        :param mapping: Optional pre-made mapping
        """

        self.mapping = mapping

    def get(self, name: str) -> Point2:
        return self.mapping[name]

    def set(self, name: str, goal: Point2):
        self.mapping[name] = goal


class Room:
    """
    Room class, containing room geometry info, tables, and obstacles
    """

    geometry  = None
    obstacles = []
    tables    = []

    __win     = None # for debug, window object

    def __init__(self, geometry: Rectangle, obstacles: List[Rectangle], tables: List[Table]):
        """
        Initialize the room

        :param geometry: Room geometry
        :type geometry: Rectangle
        :param obstacles: Obstacles in the room
        :type obstacles: List[Rectangle]
        :param tables: Tables in the room
        :type tables: List[Table]
        """
        self.geometry = geometry
        self.obstacles = obstacles
        self.tables = tables

    def __del__(self):
        """
        Destructor for this Room. should clean up connections, window, etc.
        """
        if self.__win is not None:
            self.__win.close()

    def draw(self, waitForMouse=True, colorMap={}, frame_extra=None, scale_factor=25):
        """
        Draw the current room for debugging purposes.

        Add extras in the frame_extra call--calls with the window, graphics obj, and 

        :param waitForMouse: Whether or not to wait for the mouse
        :param colorMap: dict of colors for table names (default blue)
        :param frame_extras: extension function
        """
        from server.common import graphics as g

        # helper fn: scale m to cm for display (+ margin)
        scale = lambda s: s * scale_factor


        # create the TKinter window if it doesn't exist
        if self.__win is None:
            self.__win = g.GraphWin(
                'Room viewer',
                scale(self.geometry.width),
                scale(self.geometry.height),
                autoflush=False
            )

            self.__win.setCoords(
                -5,
                -5,
                scale(self.geometry.width) + 5,
                scale(self.geometry.height) + 5
            )




        # helper function to draw a rectangle
        def drawRect(rect, outline='black'):
            # using rotation matrix (w/ rotation as origin)
            rotation = np.matrix([
                [math.cos(rect.orientation), -1 * math.sin(rect.orientation)],
                [math.sin(rect.orientation),      math.cos(rect.orientation)]
            ])

            # get the origin point of the rotation (the rectangle position)
            # we'll be transposing by this at the end of the operation
            origin = scale_factor * rect.position.as_col_vec()

            # first though, get the corner points
            p1 = rotation * (scale_factor * np.array([[ rect.width,           0 ]]).T)
            p2 = rotation * (scale_factor * np.array([[ rect.width, rect.height ]]).T)
            p3 = rotation * (scale_factor * np.array([[          0, rect.height ]]).T)

            # transpose to the rectangle origin
            p1 = origin + p1
            p2 = origin + p2
            p3 = origin + p3

            # helper to create graphics points
            createGPoint = lambda p: g.Point(*p)

            # create vertices
            vertices = map(
                    createGPoint,
                    [origin, p1, p2, p3]
            )
            vertices = list(vertices)

            # draw the polygon
            poly = g.Polygon(vertices)
            poly.setOutline(outline)
            poly.draw(self.__win)

        # draw the room boundary
        drawRect(self.geometry, outline='black')
        
        # draw the obstacles
        for obstacle in self.obstacles:
            drawRect(obstacle, outline='red')

        # draw the tables
        for table in self.tables:
            if table.name in colorMap:
                drawRect(table.geometry, outline=colorMap[table.name])
            else:
                drawRect(table.geometry, outline='blue')

        if frame_extra is not None:
            frame_extra(self.__win, g, scale)

        # update the view
        self.__win.update()

        if waitForMouse:
            self.__win.getMouse()

        # (hackily) clear the view
        for item in self.__win.items:
            item.undraw()

def randomRects(xbound, ybound, rotated=True, count_bounds=None):

    # little hack to remove rotation
    rotated = 1 if rotated else 0

    # create N random rectangles
    if count_bounds is None:
        rect_count = randint(3, 7)
    else:
        rect_count = randint(*count_bounds)

    out = []
    for i in range(rect_count):
        out.append(
            Rectangle(
                random() * (ybound / 4),
                random() * (xbound / 4),
                Point2(
                    xbound * random(),
                    ybound * random()
                ),
                random() * (math.pi * 2) * rotated
            )
        )
    return out

def randomTables(xbound, ybound):
    # wrap in a table constructor
    rects = randomRects(xbound, ybound)
    return list(map(lambda r: Table(r), rects))

if __name__ == "__main__":


    while True:
        r1 = Room(
            Rectangle(10,20, Point2(0, 0), 0),
            randomRects(10,20),
            randomTables(10,20)
        )

        r1.draw()

        del r1


