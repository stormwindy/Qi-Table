import sys
sys.path.append("../")
from server.vision.room import Room
import numpy as np
from server.pathfinding.planner import AStarPlanner
import matplotlib.pyplot as plt
import time

r = Room('room0')  # Load saved room and obstacles
# r = Room(0)        # Take a picture of the room and mark obstacles manually

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
def draw_rect(x, y, lside, sside):
    #bot
    for xx in range(lside):
        ox.append(x + xx)
        oy.append(y)
    for xx in range(lside):
        ox.append(x + xx)
        oy.append(y + sside - 1)
    for yy in range(sside):
        oy.append(y + yy)
        ox.append(x)
    for yy in range(sside):
        oy.append(y + yy)
        ox.append(x + lside - 1)
draw_rect(200, 300, 100, 200)
draw_rect(600, 700, 200, 200)
draw_rect(0, 0, 1920, 1080)
draw_rect(1000, 200, 300, 300)
draw_rect(1500, 700, 50, 50)
# start, goal
sx, sy, gx, gy = 20.0, 20.0, 1850.0, 950.0

grid_size = 30.0
robot_radius = 15.0

###

plt.plot(ox, oy, ".k")
plt.plot(sx, sy, "og")
plt.plot(gx, gy, "xb")
plt.grid(True)
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

r.draw_path(np.array([[[500, 100], [500, 600], [600, 600]]]))
# r.show(True)



