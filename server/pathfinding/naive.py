# Naive antigravity pathfinding
# author: patrick kage
import sys
sys.path.append('../..')

from base import *
import numpy as np
from collections import deque
import math
import time

MAX_NEGATIVE_FORCE    = 6
OBSTACLE_REPULSE_AREA =  1.25 # meters
GOAL_FORCE            =  5
STEP_SIZE             =  0.1  # meters
SAFETY_MARGIN         =  0.15 # meters
CRISIS_HISTORY        = 5     # moves
CRISIS_TRIGGER        = 2     # steps

class Pathfinder:

    frozen = set([])
    goaled = set([])
    crisis = set([])

    # history
    history = {}

    def __init__(self):
        """
        Initialize the pathfinder
        """
        self.frozen = set([])
        self.goaled = set([])

    def get_centroid(self, rect: Rectangle):
        # TODO: rotation
        return Point2(
            rect.position.x + (rect.width / 2),
            rect.position.y + (rect.height / 2)
        )

    def get_radius(self, rect: Rectangle):
        # pythagorean
        return SAFETY_MARGIN + math.sqrt( math.pow(rect.width, 2) + math.pow(rect.height, 2) ) / 2

    #def get_obstacle_vector(self, centroid: Point2, radius, from_position: Point2):
    def get_obstacle_vector(self, obstacle: Rectangle, table: Rectangle):
        """
        Get obstacle vector, defined as a piecewise function.
        Essentially a linear shifted to the right and tweaked for
        room-scale, with a piecewise component to clip to maximum force and zero

        :param centroid: Object center (numpy vec)
        :param radius:   Radius of the object (float)
        :param from_position: your position (numpy vec)
        :returns: a scaled vector pointing away from the obstacle, 
        """

        # TODO: rotation
        o_centroid = self.get_centroid(obstacle).as_col_vec()
        t_centroid = self.get_centroid(table).as_col_vec()
        
        def pythag(a,b):
            return math.sqrt( math.pow(a, 2) + math.pow(b, 2) )

        radius = self.get_radius(obstacle) + self.get_radius(table)

        # calculate distances
        distance = np.linalg.norm(o_centroid - t_centroid)

        # make sure we haven't clipped inside the object
        if distance <= radius:
            force = MAX_NEGATIVE_FORCE
        elif distance + radius < OBSTACLE_REPULSE_AREA:


            # from 0 to radius: MAX_NEGATIVE_FORCE
            # from radius to radius + OBSTACLE_REPULSE_AREA: linear
            # zero otherwise

            # F = m ((distance - radius) - OBSTACLE_REPULSE_AREA)
            #  where
            #    m = dropoff slope
            #    b = MAX_NEGATIVE_FORCE
            slope = MAX_NEGATIVE_FORCE / OBSTACLE_REPULSE_AREA

            force = slope * ( (distance - radius) - OBSTACLE_REPULSE_AREA)
        else:
            force = 0

        # clip to zero if negative to avoid attracting to objects
        force = max( 0, force)
        


        # get the direction vector and normalize it
        obstacle_vec = t_centroid - o_centroid
        obstacle_vec = obstacle_vec / np.linalg.norm(obstacle_vec)

        # multiply the direction by the force
        obstacle_vec *= force

        return obstacle_vec

    def __determine_freeze(self, room, table):
        for other in room.tables:
            if other.name == table.name:
                continue
            if other.name in self.frozen:
                continue

            # TODO: take radii into account
            if table.geometry.position.distanceTo(other.geometry.position) < 2:
                return True

        if table.name in self.frozen:
            shouldUnfreeze = False
            for other in room.tables:
                if other.name == table.name:
                    continue
                if table.geometry.position.distanceTo(other.geometry.position) < 3:
                    shouldUnfreeze = True
            return shouldUnfreeze

        return False


    def __within_goal(self, table, goal):
        if table.geometry.position.distanceTo(goal) < 2 * STEP_SIZE:
            self.goaled.add(table.name)
            return True
        return False


    def get_goal_vector(self, from_position: Point2, goal_position: Point2):
        """
        get_goal_vector

        :param from_position: 
        :param goal_position: 
        """

        # get the direction vector and normalize it
        goal_vec = (goal_position.as_col_vec() - from_position.as_col_vec())
        goal_vec = goal_vec / np.linalg.norm(goal_vec)

        # multiply the direction by the force
        goal_vec *= GOAL_FORCE

        return goal_vec

    def get_vec_for_point(room, name):
        pass
        
    def __log_move(self, tname, movement):
        # log the moves

        self.history[tname].append(movement)

        # ensure we keep $CRISIS_HISTORY moves
        if len(self.history[tname]) == CRISIS_HISTORY:
            self.history[tname].pop(0)

    def __calculate_crisis(self, tname, vecs):
        if tname not in self.history:
            self.history[tname] = []

        # if we're in crisis, figure out how far we've made it
        vec = np.sum(self.history[tname], axis=0)
        dist = np.linalg.norm(vec)

        # figure out our crisis state
        if tname in self.crisis:
            if dist > STEP_SIZE * CRISIS_HISTORY:
                self.crisis.discard(tname)
            else:
                # rotate goal vec 90deg
                rotate = np.array([[ 1, 0 ], [ 0, -1]])
                vecs[0] = np.dot(rotate, vecs[0])
        else:
            if dist < STEP_SIZE * CRISIS_TRIGGER:
                self.crisis.add(tname)

        return vecs

    def pathfind(self, room, layout):
        """
        Pathfind

        :param room: Room object
        :param layout: Layout object
        """

        # TODO: execute tables in order of how close they are to the goal

        
        for table in room.tables:
            # check if we're done
            if self.__within_goal(table, layout.get(table.name)):
                continue

            # check the frozen status
            if self.__determine_freeze(room, table):
                self.frozen.add(table.name)
            else:
                self.frozen.discard(table.name)

            if table.name in self.frozen:
                continue

            # calculate all the force vectors, starting with the goal vec (should be first)
            vecs = [ 
                self.get_goal_vector(table.geometry.position, layout.get(table.name) )
            ]


            # ... then the obstacle vectors
            for obstacle in room.obstacles:
                vecs.append(self.get_obstacle_vector(obstacle, table.geometry))

            # ... then the other tables
            for other in room.tables:
                if other.name == table.name:
                    continue
                vecs.append(
                    self.get_obstacle_vector(
                        other.geometry,
                        table.geometry
                    )
                )


            # create the result vector, normalize, and scale
            movement = np.sum(vecs, axis=0) # sum along rows
            movement = movement / np.linalg.norm(movement)
            movement = movement * STEP_SIZE

            # move
            table.geometry.position.x += movement[0][0]
            table.geometry.position.y += movement[1][0]

            
        return room

if __name__ == '__main__':
    # set up a demo room
    
    obstacles = [
        Rectangle(
            3,
            2,
            Point2(3,4),
            0
        ),
        Rectangle(
            3,
            2,
            Point2(10,7),
            0
        )
    ]

    tables = [
        Table(
            Rectangle(1,1,Point2(1,3), 0),
            name='table1'
        ),
        Table(
            Rectangle(1,1,Point2(1,10), 0),
            name='table2'
        )
    ]

    obstacles = randomRects(10,20, rotated=False, count_bounds=(10,20))

    layout = Layout( {
        'table1': Point2(19, 11),
        'table2': Point2(19, 2)
    } )

    room = Room(
        Rectangle(22, 13, Point2(0,0), 0),
        obstacles,
        tables
    )

    pathfinder = Pathfinder()

    def mapColors(pf):
        out = {}
        for n in pf.frozen:
            out[n] = 'orange'
        for n in pf.goaled:
            out[n] = 'green'
        return out

    def draw_bound(rect, pf, win, g, scale):
        center = pf.get_centroid(rect)
        radius = pf.get_radius(rect)
        bound  = g.Circle(
            g.Point(scale(center.x), scale(center.y)),
            scale(radius)
        )
        bound.setOutline('purple')
        bound.draw(win)

    def draw_field(room, pf, win, g, scale):
        pass

    while True:
        exec_time = time.time()
        room = pathfinder.pathfind(room, layout)
        exec_time = time.time() - exec_time

        def frame_extra(win, g, scale):
            # frame timing
            text = g.Text(g.Point(
                win.getWidth() / 2,
                10
            ), '{:.3} ms'.format(exec_time * 1000))
            text.setTextColor('green')
            text.draw(win)

            # draw goals
            for name in layout.mapping:
                goal = layout.get(name)
                g1 = g.Circle(g.Point(scale(goal.x + 0.5), scale(goal.y + 0.5)), scale(0.2))
                g1.setOutline('green')
                g1.draw(win)

            # draw bounds
            for table in room.tables:
                draw_bound(table.geometry, pathfinder, win, g, scale)

            for obstacle in room.obstacles:
                draw_bound(obstacle, pathfinder, win, g, scale)


        room.draw(
            waitForMouse=False,
            colorMap=mapColors(pathfinder),
            scale_factor=50,
            frame_extra=frame_extra
        )
        time.sleep(0.05)

