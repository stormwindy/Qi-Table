import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../../../..'))
import pickle
from server.vision.camera import Camera
import numpy as np

NUM = 10

# Load camera parameters
dirname = os.path.abspath(__file__ + "/../../..")
param = pickle.load(open(os.path.join(dirname, 'camera_param' + '.p'), "rb"))
mtx, dist, rvecs, tvecs = param[0], param[1], param[2], param[3]

camera = Camera(1)

def center(pos: np.ndarray) -> np.ndarray:
    res = np.zeros(2)
    for p in pos:
        res += p
    return res/4


pos = camera.get_pos(NUM)
realPos = dict()
for i in range(1,NUM+1):
    realPos[i] = center(pos[i])
d = []
for i in range(1,NUM):
    d.append(np.sqrt(np.sum((realPos[i] - realPos[i + 1])**2)))
np.set_printoptions(precision=3)
d = np.array(d)
avg = np.average(d)
print(d,avg)
