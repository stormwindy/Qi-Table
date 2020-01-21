#! /usr/bin/env python

import math
from typing import 

class Point2:
    """
    Point2: Generic 2D point
    """
    x = None
    y = None

    def __init__(self, x: float, y: float) -> Point2:
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

    def distanceTo(self, point: Point2) -> float:
        """
        distanceTo: Calculate the L2 norm from this point to another

        :param point: The other point
        :type point: Point2
        :rtype: float
        """
        return math.sqrt(
                math.pow( self.x - point.y, 2) +
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

    def intersects(self, rect: Rectangle) -> bool:
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
    
    def __init__(self, geometry: Rectangle):
        """
        Initialize the table.

        :param geometry: Table geometry.
        :type geometry: Rectangle
        """
        self.geometry = geometry

