import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../..'))
from server.vision.room import Room
import numpy as np
from server.pathfinding.planner import AStarPlanner
import matplotlib.pyplot as plt
import time




r = Room('room0')  # Load saved room and obstacles
# r = Room(1)        # Take a picture of the room and mark obstacles manually
# ox, oy = AStarPlanner.vertices_to_lines(r.obsts)
# add border
ox, oy = [], []

'''
Some notes for you Ege:

1. draw_rect() below makes rectangular obstacles by putting 
the coordinates of the points on the sides into ox and oy

Currently, it takes the bottom-left corner (x, y) and the length of the sides (lside, sside)
as parameters. But I want it to take instead two coordinates, that are 
any two vertices that oppose each other (they define a rectangle)
The new function should look like:

def function_name(vertex1: Tuple[int, int], vertex2: Tuple[int, int]) -> None:

2. It is good if you also read through pathfinding/planner.py, if might be helpful
when tuning the grid_size and robot_radius

3. The initializtion currently takes a longtime (as timed below), but that can be 
serialized, so don't worry about that. Or you can change planner.py's constructor
so it can load serialized objects (preferably simliar to how I did in room.py)
'''

def draw_rect(pt1, pt2):
    # Bottom left
    bl_x, bl_y = pt1[0], pt1[1]
    # Top right
    tr_x, tr_y = pt2[0], pt2[1]

    # Horizontal side length
    hside = tr_x - bl_x + 1
    # Vertical side length
    vside = tr_y - bl_y + 1

    # Insert the coordinates to ox, oy
    for i in range(hside):  # Top and bottom sides
        ox.append(bl_x + i)
        oy.append(bl_y)
        ox.append(bl_x + i)
        oy.append(tr_y)
    for j in range(vside):
        ox.append(bl_x)
        oy.append(bl_y + j)
        ox.append(tr_x)
        oy.append(bl_y + j)



for pt1, pt2 in r.obsts.values():
    draw_rect(pt1, pt2)
# start, goal
sx, sy, gx, gy = 460.0, 530.0, 1430.0, 800.0


grid_size = 32.0
robot_radius = 130.0

###
plt.imshow(r.frame_orig)
plt.plot(ox, oy, ".k")
plt.plot(sx, sy, "og")
plt.plot(gx, gy, "xb")
plt.grid(False)
plt.axis("equal")

t1 = time.time()
a_star = AStarPlanner(ox, oy, grid_size, robot_radius)
t2 = time.time()
print(t2-t1)
rx, ry = a_star.planning(sx, sy, gx, gy)
t3 = time.time()
print(t3 - t2)

plt.plot(rx, ry, "-r")
plt.show()

# r.draw_path(np.array([[[500, 100], [500, 600], [600, 600]]]))
# r.show(True)



