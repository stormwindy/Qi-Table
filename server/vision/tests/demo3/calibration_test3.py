import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../../../..'))
import pickle
from server.vision.camera import Camera
import numpy as np
from numpy.linalg import norm
import math

NUM = 9

# Load camera parameters
dirname = os.path.abspath(__file__ + "/../../..")
param = pickle.load(open(os.path.join(dirname, 'camera_param' + '.p'), "rb"))
mtx, dist, rvecs, tvecs = param[0], param[1], param[2], param[3]

camera = Camera(1)

def angle(pos: np.ndarray) -> np.ndarray:
    v1 = pos[0] - pos[3]
    v2 = np.array([10,0])
    nom = norm(np.cross(v1, v2))
    denom = norm(v1) * norm(v2)
    return math.degrees(math.asin(nom/denom))


pos = camera.get_pos(NUM)
angles = []
for i in range(1,NUM+1):
    angles.append(angle(pos[i]))

np.set_printoptions(precision=3)
angles = np.array(angles)
avg = np.average(angles)
print(angles,avg)