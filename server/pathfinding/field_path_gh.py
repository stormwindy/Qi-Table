"""

adding negative fields to the paths that are already moving

Potential Field based path planner

author: Atsushi Sakai (@Atsushi_twi)

Ref:
https://www.cs.cmu.edu/~motionplanning/lecture/Chap4-Potential-Field_howie.pdf

"""

import numpy as np
import matplotlib.pyplot as plt
#from table_functions import *
from base import *

# Parameters
KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain
# AREA_WIDTH = 30.0  # potential area width [m]

ROOM_WIDTH = 70
ROOM_HEIGHT = 50

# camera = Camera(1)

show_animation = True


def calc_potential_field(gx, gy, ox, oy, reso, rr):
    # minx = min(ox) - AREA_WIDTH / 2.0
    # miny = min(oy) - AREA_WIDTH / 2.0
    # maxx = max(ox) + AREA_WIDTH / 2.0
    # maxy = max(oy) + AREA_WIDTH / 2.0
    # xw = int(round((maxx - minx) / reso))
    # yw = int(round((maxy - miny) / reso))

    xw = int(round(ROOM_WIDTH / reso)) # potential field size width
    yw = int(round(ROOM_HEIGHT / reso)) # potential field height

    # calc each potential
    pmap = [[0.0 for i in range(yw)] for i in range(xw)]

    for ix in range(xw):
        x = ix * reso

        for iy in range(yw):
            y = iy * reso
            # add negative field to the cells near the walls
            if (ix == 0 or iy == 0 or ix == xw - 1 or iy == yw - 1):
                ug = 0
                uo = -1 # adjust the negative value later
            else:
                ug = calc_attractive_potential(x, y, gx, gy)
                uo = calc_repulsive_potential(x, y, ox, oy, rr)
            uf = ug + uo
            pmap[ix][iy] = uf

    return pmap #, minx, miny


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


def get_motion_model():
    # dx, dy
    motion = [[1, 0],
              [0, 1],
              [-1, 0],
              [0, -1],
              [-1, -1],
              [-1, 1],
              [1, -1],
              [1, 1]]

    return motion


def potential_field_planning(sx, sy, gx, gy, ox, oy, reso, rr):

    # calc potential field
    pmap = calc_potential_field(gx, gy, ox, oy, reso, rr)

    # search path
    d = np.hypot(sx - gx, sy - gy)
    ix = round(sx / reso)
    iy = round(sy / reso)
    gix = round(gx / reso)
    giy = round(gy / reso)

    if show_animation:
        draw_heatmap(pmap)
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
        plt.plot(ix, iy, "*k")
        plt.plot(gix, giy, "*m")
        # plt.show()

    rx, ry = [sx], [sy]
    motion = get_motion_model()
    #distance to goal >= grid size
    while d >= reso:
        minp = float("inf")
        minix, miniy = -1, -1
        for i, _ in enumerate(motion):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            if inx >= len(pmap) or iny >= len(pmap[0]):
                p = float("inf")  # outside area
            else:
                p = pmap[inx][iny]
            if minp > p:
                # indices of minimum potentials
                minp = p
                minix = inx
                miniy = iny
        ix = minix
        iy = miniy
        xp = ix * reso
        yp = iy * reso
        d = np.hypot(gx - xp, gy - yp)
        rx.append(xp)
        ry.append(yp)

        if show_animation:
            plt.plot(ix, iy, ".r")
            plt.pause(0.01)

    print("Goal!!")

    return rx, ry



def my_potential_field_planning(table, gx, gy, ox, oy, reso, rr):

    # calc potential field
    pmap = calc_potential_field(gx, gy, ox, oy, reso, rr)

    sx = table.geometry.central_position.x
    sy = table.geometry.central_position.y

    # search path
    d = np.hypot(sx - gx, sy - gy)
    ix = round(sx / reso)
    iy = round(sy / reso)
    gix = round(gx / reso)
    giy = round(gy / reso)

    if show_animation:
        draw_heatmap(pmap)
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
        plt.plot(ix, iy, "*k")
        plt.plot(gix, giy, "*m")
        # plt.show()

    rx, ry = [sx], [sy]
    motion = get_motion_model()

    while d >= reso:
        minp = float("inf")
        minix, miniy = -1, -1
        for i, _ in enumerate(motion):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            if inx >= len(pmap) or iny >= len(pmap[0]):
                p = float("inf")  # outside area
            else:
                p = pmap[inx][iny]
            if minp > p:
                # indices of minimum potentials
                minp = p
                minix = inx
                miniy = iny
        ix = minix
        iy = miniy
        xp = ix * reso
        yp = iy * reso

        # while

        d = np.hypot(gx - xp, gy - yp)
        rx.append(xp)
        ry.append(yp)

        if show_animation:
            plt.plot(ix, iy, ".r")
            plt.pause(0.01)

    print("Goal!!")

    return rx, ry


def move():

    # pos = self.camera.get_pos(1) # to get table position from vision
    # ar1, ar2 = pos[1]
    # table = form_table(ar1, ar2, 1)

    rectangle = Rectangle(5, 3, Point2(17.5, 38.5), 0, Point2(15, 40), Point2(15, 37), Point2(20, 40), Point2(20, 37))
    table = Table(rectangle, 1)
    # table radius
    radius = diagonal(table) / 2.0


    # self.camera.release()


def draw_heatmap(data):
    data = np.array(data).T
    plt.pcolor(data, vmax=100.0, cmap=plt.cm.Blues)


def main():
    print("potential_field_planning start")
    #
    sx = 5.0  # start x position [m]
    sy = 10.0  # start y positon [m]
    gx = 30.0  # goal x position [m]
    gy = 30.0  # goal y position [m]
    grid_size = 0.5  # potential grid size [m]
    robot_radius = 3.0  # robot radius [m]

    ox = [15.0, 5.0, 20.0, 25.0, ]  # obstacle x position list [m]
    oy = [25.0, 15.0, 26.0, 25.0]  # obstacle y position list [m]

    if show_animation:
        plt.grid(True)
        plt.axis("equal")

    # path generation
    rx, ry = potential_field_planning(
        sx, sy, gx, gy, ox, oy, grid_size, robot_radius)

    print(rx, ry)


    if show_animation:
        plt.show()



if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")
