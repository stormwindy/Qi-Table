import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../../../..'))
import cv2
import pickle



dirname = os.path.abspath(__file__ + "/../../..")
param = pickle.load(open(os.path.join(dirname, 'camera_param' + '.p'), "rb"))
mtx, dist, rvecs, tvecs = param[0], param[1], param[2], param[3]

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', (1280, 720))
frame = cv2.imread(os.path.join(dirname, 'checkerboards', 'board33.png'))
undistorted = cv2.undistort(frame, mtx, dist)
cv2.imshow('frame', frame)
cv2.waitKey(0)
cv2.imshow('frame', undistorted)
cv2.waitKey(0)
cv2.destroyAllWindows()