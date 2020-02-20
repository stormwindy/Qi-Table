
import numpy as np
import matplotlib.pyplot as plt

# Parameters
KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain
#AREA_WIDTH = 30.0  # potential area width [m]


room_width = 25
room_height = 15

show_animation = True




def calc_potential_field(gx, gy, ox, oy, reso, rr):
    print (' gw , gy : ' , gx , gy )


    # minx = min(ox) - AREA_WIDTH / 2.0
    # print ( 'minx' , minx)
    # miny = min(oy) - AREA_WIDTH / 2.0
    # print('miny', miny)
    # maxx = max(ox) + AREA_WIDTH / 2.0
    # maxy = max(oy) + AREA_WIDTH / 2.0
    # print(' maxx , maxy ' , maxx , maxy)
    xw = int(round( room_width / reso))
    yw = int(round( room_height / reso))
    # print('xw , yw ' , xw , yw)
    # # calc each potential
    # pmap = [[0.0 for i in range(yw)] for i in range(xw)]

    cmap =  [[0.0 for i in range(yw)] for i in range(xw)]
    print(' Here we enter the for loop')
    for ix in range(xw):
        x = ix * reso

        print( 'we enter the loop with x , where x = ix * reso  and  y = iy * reso ' )
        print( 'x = ', ix , ' * ' , reso , ' = ' , x)
        for iy in range(yw):
            y = iy * reso
            print (' x y = ',x , y)

            ug = calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr)
            uf = ug + uo

            cmap[ix][iy] = uf

            print('cmap[',ix,'][',iy,'] =' , uf)

    return cmap


def calc_potential_field_nextcell(cell_x, cell_y , gx, gy, ox, oy, reso , rr, nmap):
    # create 3 x 3 matrix to only represent the gird cells around the table centre position
    #we are assuming that current_x and current_y are cell position and not coordinates, therefore we need to convert it
    nlist = []
    minp = float(inf)
    minix, miniy = -1, -1
    for ix in range((cell_x - 1), (cell_x+2)):
        for iy in range((cell_y - 1), (cell_y+2)):
            print(' x y = ', ix, iy)
            ug = calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr)
            uf = ug + uo
            nmap[ix][iy] = uf #adds the nrighbour potentials to the room map/grid
            nlist.append(uf)  #adds the neighbour potentials to a list  (8 elements)
            if ix >= room_x or iy >= room_y:
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


def path_sequence(sx, sy, gx, gy, reso, rr):


    room_x = int(round(room_width / reso))
    room_y = int(round(room_height / reso))

    # start and end cell
    ix = round(sx / reso)
    iy = round(sy / reso)
    gix = round(gx / reso)
    giy = round(gy / reso)
    cmap = [[0.0 for i in range(yw)] for i in range(xw)]
    d = np.hypot(sx - gx, sy - gy)

    #rx, ry = [sx], [sy]
    coord_path = []  # coord_path = [ (x1,y1), (x2,y2) ...... ] sequence of coordinate movements

    #motion = get_motion_model()
    while d >= reso:

        _, _, minix, miniy =  calc_potential_field_nextcell(ix, iy, gx, gy, ox, oy, reso, rr, nmap)
        ix , iy = minix , miniy
        xp = minix * reso
        yp = miniy * reso
        coord_path.append((minx, miny))
        d = np.hypot(gx - xp, gy - yp)
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


def main():
    print("potential_field_planning start")

    sx = 0.0  # start x position [m]
    sy = 10.0  # start y positon [m]
    gx = 30.0  # goal x position [m]
    gy = 30.0  # goal y position [m]
    grid_size = 0.5  # potential grid size [m]
    robot_radius = 5.0  # robot radius [m]


    grid_size = 1
    cell_path = []  # cell_path = [ (ix1,iy1), (ix2,iy2) ... ] sequence of cell movements

    
    ox = [15.0, 5.0, 20.0, 25.0]  # obstacle x position list [m]
    oy = [25.0, 15.0, 26.0, 25.0]  # obstacle y position list [m]

    if show_animation:
        plt.grid(True)
        plt.axis("equal")

    # path generation
    _, _ = potential_field_planning(
        sx, sy, gx, gy, ox, oy, grid_size, robot_radius)

    if show_animation:
        plt.show()


if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")