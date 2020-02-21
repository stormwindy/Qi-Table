
import numpy as np
import matplotlib.pyplot as plt

# Parameters
from base import *
from server.pathfinding.table_functions import *
from server.vision.camera import Camera

KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain
#AREA_WIDTH = 30.0  # potential area width [m]
cell_path = []  # cell_path = [ (ix1,iy1), (ix2,iy2) ... ] sequence of cell movements

room_width = 25
room_height = 15
room_x = 0
room_y = 0
show_animation = True

camera = Camera(0)


def calc_potential_field_nextcell(cell_x, cell_y , gx, gy, ox, oy, reso , rr, nmap):
    # create 3 x 3 matrix to only represent the gird cells around the table centre position
    #we are assuming that current_x and current_y are cell position and not coordinates, therefore we need to convert it
    nlist = []

    minp = float("inf")
    minix, miniy = -1, -1
    for ix in range((cell_x - 1), (cell_x+2)):
        x = ix * reso
        for iy in range((cell_y - 1), (cell_y+2)):
            print(' ix iy = ', ix, iy)
            y = iy * reso
            ug = calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr)
            uf = ug + uo
            nmap[ix][iy] = uf #adds the neighbour potentials to the room map/grid
            nlist.append(uf)  #adds the neighbour potentials to a list  (8 elements)
            if ix >= len(nmap) or iy >= len(nmap[0]):
                p = float("inf")  # outside area
            else:
                p = nmap[ix][iy]
                # or
                # p = uf
            if minp > p:
                minp = p
                minix = ix
                miniy = iy
    cell_path.append((minix, miniy))
    return nmap, nlist, minix, miniy





def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * KP * np.hypot(x - gx, y - gy)


def calc_repulsive_potential(x, y, ox, oy, rr):
    # search nearest obstacle
    minid = -1
    dmin = float("inf")
    for i, _ in enumerate(ox):
        d = np.hypot(x - ox[i], y - oy[i])
        if dmin >= d:
            dmin = d
            minid = i

    # calc repulsive potential
    dq = np.hypot(x - ox[minid], y - oy[minid])

    #rr -> rr*2 for safe distance between tables (distance between tables is the distance btw their centres)
    if dq <= (rr*2):
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


def path_sequence(sx, sy, gx, gy, ox, oy, reso, rr):


    room_x = int(round(room_width / reso))
    room_y = int(round(room_height / reso))

    # start and end cell
    ix = round(sx / reso)
    iy = round(sy / reso)
    gix = round(gx / reso)
    giy = round(gy / reso)
    xw = int(round(room_width / reso))
    yw = int(round(room_height / reso))
    nmap = [[0.0 for i in range(yw)] for i in range(xw)]
    d = np.hypot(sx - gx, sy - gy)

    #rx, ry = [sx], [sy]
    coord_path = []  # coord_path = [ (x1,y1), (x2,y2) ...... ] sequence of coordinate movements

    #motion = get_motion_model()
    while d >= reso:
        #ox and oy represent static obstacles
        #tx and ty represent the centre coordinates of the tables (dynamic)
        tx , ty = get_table_centres()
        otx = ox + tx
        oty = oy + ty
        newmap, _, minix, miniy =  calc_potential_field_nextcell(ix, iy, gx, gy, otx, oty, reso, rr, nmap)
        ix , iy = minix , miniy
        xp = minix * reso
        yp = miniy * reso
        coord_path.append(Point2(xp, yp))
        d = np.hypot(gx - xp, gy - yp)
        nmap = newmap
        #rx and ry are the same as coord_path = [ (x1,y1), (x2,y2) ... ]
        # rx.append(xp)
        # ry.append(yp)
        # plt.plot(ix, iy, ".r")
        # plt.pause(0.01)
    print(coord_path)
    print("Goal!!")


    return coord_path


def draw_heatmap(data):
    data = np.array(data).T
    plt.pcolor(data, vmax=100.0, cmap=plt.cm.Blues)

def get_table_centres():
    # calculates the new obstacles(table_centres)
    tx = []
    ty = []
    pos = camera.get_pos(3)
    for id in pos:
        ar1, ar2 = pos[id]
        table_coord = table_centre(Point2(ar1[0], ar1[1]), Point2(ar2[0], ar2[1]))
        # or
        # centre_x = (ar1[0] + ar2[0]) / 2
        # centre_y = (ar1[1] + ar2[1]) / 2
        tx.append(table_coord.x)
        ty.append(table_coord.y)

    return tx , ty


def main():
    print("potential_field_planning start")

    sx = 0.0  # start x position [m]
    sy = 10.0  # start y positon [m]
    start = Point2(sx,sy)
    gx = 30.0  # goal x position [m]
    gy = 30.0  # goal y position [m]
    goal = Point2(gx,gy)
    grid_size = 0.5  # potential grid size [m]
    robot_radius = 5.0  # robot radius [m] (1/2 of the table_width)

    #static obstacles
    ox = [15.0, 5.0, 20.0, 25.0]  # obstacle x position list [m]
    oy = [25.0, 15.0, 26.0, 25.0]  # obstacle y position list [m]
    #path_generation
    path = path_sequence(sx,sy,gx,gy,ox,oy,grid_size,robot_radius)

    # find a way to move table to final goal position)
    #if(np.hypot(path[-1] , goal) > 0.0)
    # do something


    print(path)

    #
    # if show_animation:
    #     plt.grid(True)
    #     plt.axis("equal")



    if show_animation:
        plt.show()


if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")