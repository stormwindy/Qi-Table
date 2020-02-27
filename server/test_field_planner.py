import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../..'))
from server.vision.room import Room
import numpy as np
from server.pathfinding.planner import AStarPlanner
from server.pathfinding.field_path import FieldPlanner
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time




r = Room('room0')  # Load saved room and obstacles
# add border
ox, oy = [], []

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

obstacles = r.obsts
room_width, room_height = obstacles[0][1]
obstacles.pop(0) #remove room bounds
potential_field = FieldPlanner(room_width, room_height, obstacles, grid_size, robot_radius)
potential_field.set_table_centres([(sx, sy)])
paths = potential_field.plan([(gx, gy)])
rx, ry = paths[1]

ax = plt.gca()

for i in range(4):
    plt.plot(potential_field.ox[i], potential_field.oy[i], marker="*", color="gold")
radius = potential_field.orad
for i in range(len(radius)):
    circle = Circle((potential_field.ox[i], potential_field.oy[i]), radius[i], color="gold", fill=False)
    ax.add_patch(circle)
plt.plot(rx, ry, "-r")
plt.show()
