"""

adding negative fields to the paths that are already moving

Potential Field based path planner

author: Atsushi Sakai (@Atsushi_twi)

Ref:
https://www.cs.cmu.edu/~motionplanning/lecture/Chap4-Potential-Field_howie.pdf

"""

import numpy as np
import matplotlib.pyplot as plt
from table_functions import *

import sys
sys.path.append("..\\..\\")
from base import Table, Point2, Rectangle
from server.vision.camera import Camera

# TO DO: set up these as command line arguments
# Parameters
KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain

# TO DO: set up these as command line arguments
ROOM_WIDTH = 70;
ROOM_HEIGHT = 50;

camera = Camera(1)


def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * KP * np.hypot(x - gx, y - gy)


def calc_repulsive_potential(x, y, ox, oy, rr):
    # search nearest obstacle
    minid = -1
    dmin = float("inf")
    for i, _ in enumerate(ox):
        d = np.hypot(x - ox[i], y - oy[i])  # distance to obstacle
        if dmin >= d:
            dmin = d
            minid = i

    # calc repulsive potential
    dq = np.hypot(x - ox[minid], y - oy[minid])

    if dq <= rr:
        if dq <= 0.1:
            dq = 0.1

        return 0.5 * ETA * (1.0 / dq - 1.0 / rr) ** 2
    else:
        return 0.0


def my_get_motion_model():
    # changed to a list of tuples in order to form a dictionary
    # dx, dy
    motion = [(1, 0),  # right
              (0, 1),  # down
              (-1, 0),  #left
              (0, -1),  # up
              (-1, -1),  # diagonal up-left
              (-1, 1),  # diagonal down-left
              (1, -1),  # diagonal up-right
              (1, 1)]  # diagonal down-right

    # direction of movements depending on which motion is selected for the next step
    # probably will need to change values!!! also values depend on the reference frame we will be using
    # I have selected these assuming angle zero means the table's width is parallel to the x axis
    # and positive rotation is clockwise;
    # however it would be better if these match with the orientation of the table
    angles = [0.0, 90.0, 0.0, 90.0, 45.0, -45.0, -45.0, 45.0]
    motion_angles = dict(zip(motion, angles))

    return motion, motion_angles


# sx = current x position of table centre
# sy = current y position of table centre
def calc_potential_field_for_table(sx, sy, gx, gy, ox, oy, rr):

    # create 3 x 3 matrix to only represent the gird cells around the table centre position
    pmap = np.zeros((3, 3))
    for x in range(3):
        for y in range(3):
            ug = calc_attractive_potential(sx, sy, gx, gy)
            uo = calc_repulsive_potential(sx, sy, ox, oy, rr)
            uf = ug + uo
            pmap[x][y] = uf

    return pmap

def my_potential_field_planning(ar1, ar2, gx, gy, ox, oy, reso):

    table = form_table(ar1, ar2, 1)

    sx = table.geometry.central_position.x
    sy = table.geometry.central_position.y
    rr = diagonal(table) / 2.0

    # adds room boundaries: table centre position can't come closer to the wall than its radius
    grid_bound_left = int(round(rr / reso)) # number of cells the radius takes
    grid_bound_right = int(round(ROOM_WIDTH / reso - rr / reso))
    grid_bound_top = int(round(rr / reso))
    grid_bound_bottom = int(round(ROOM_HEIGHT / reso - rr /reso))

    # search path
    d = np.hypot(sx - gx, sy - gy)
    ix = round(sx / reso)
    iy = round(sy / reso)

    rx, ry = [sx], [sy]
    motion, angles = my_get_motion_model()

    while d >= reso:
        minp = float("inf")
        minix, miniy = -1, -1
        dir = (0, 0)
        for i, _ in enumerate(motion):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            # calc potential field
            pmap = calc_potential_field_for_table(sx, sy, gx, gy, ox, oy, rr)
            if inx >= grid_bound_right or inx <= grid_bound_left \
                    or iny >= grid_bound_bottom or iny <= grid_bound_top:
                p = float("inf")  # outside area
            else:
                p = pmap[motion[i][0]][motion[i][1]]
            if minp > p:
                # indices of minimum potentials
                minp = p
                minix = inx
                miniy = iny
                # get the direction the robot needs to move to
                dir = motion[i]
        ix = minix
        iy = miniy
        xp = ix * reso
        yp = iy * reso

        angle = angles[dir] #direction of movement
        orientation = table.geometry.orientation

        id = table.table_id
        if not angle == orientation :
          # TO-DO: send direction to robot to rotate
            # OR INSTEAD OF BELLOW while not (angle >= orientation - 1 and angle <= orientation + 1) : #added 1s for errors???
          while not angle == orientation :
              pos = camera.get_pos(1)
              ar1, ar2 = pos[id]
              table = form_table(ar1, ar2)
              orientation = table.geometry.orientation
              # would be good to have function get_orientation() probs easy to extract that part from form_table
              orientation = get_orientation()
            # TO-DO: stop the rotation

        table.orientation = angle # or new orientation

        if not xp == sx and xy == sy :
            # TO-DO: send directions to the table to move forwards or backwards
          while not (xp > sx - 0.5 and xp < sx + 0.5 and yp > sy - 0.5 and yp < sy + 0.5) :
              pos = camera.get_pos(1)
              ar1, ar2 = pos[id]
              new_centre = table_centre(ar1, ar2)
              sx = new_centre.x
              sy = new_centre.y
          # TO-DO: stop the movement

        # table.geometry.x = sx
        # table.geometry.y = sy

        d = np.hypot(gx - xp, gy -yp)
        rx.append(xp)
        ry.append(yp)

    # camera.release()
    print (rx, ry)
    return rx, ry


def main():
    print("potential_field_planning start")
    # TO-DO: goal position as a command line argument
    gx = 40.0  # goal x position [m]
    gy = 40.0  # goal y position [m]
    grid_size = 0.5  # potential grid size [m]

    # TO-DO: coordinates need to be taken from camera
    ox = [15.0, 5.0, 20.0, 25.0]  # obstacle x position list [m]
    oy = [25.0, 15.0, 26.0, 25.0]  # obstacle y position list [m]

    ar1 = Point2(5, 15)
    ar2 = Point2(20, 15)

    rx, ry = my_potential_field_planning(ar1, ar2, gx, gy, ox, oy, grid_size)

    print("rx : ", rx, "\n")
    print("ry : ", ry, "\n")



if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")
