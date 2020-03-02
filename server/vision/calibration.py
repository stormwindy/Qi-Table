import cv2
import os
import glob
import numpy as np
import pickle

'''
Please DO NOT execute this file.
'''

# If set to true, display all the valid checkerboards
SHOW = False
# If set to true, load serialized camera parameters
LOAD = True

# Using a 5x7 checkerboard, see checkerboards/board9.png for an example
CHECKERBOARD = (5,7)

# This is the termination criteria for cornerSubPix. It refines corners' coordinates.
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# These 3D coordinates represent the dimensions in the real world
# The side of a square on the checkerboard is 0.1078 meter
objp = np.zeros((5*7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2) * 0.1078

objpoints = [] # 3d point in real world space, will always be objp in our case.
imgpoints = [] # 2d points in image plane, coordinates captured by the camera.

images = glob.glob('./checkerboards/*.png')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    # If found, add object points, image points.
    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        if SHOW:
            # Draw and display the corners
            cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
            cv2.namedWindow('img', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('img', (1280,720))
            cv2.imshow('img', img)
            cv2.waitKey(200)

cv2.destroyAllWindows()

# Calibrate the camera using captured results
if LOAD:
    dirname = os.path.abspath(__file__ + "/..")
    param = pickle.load(open(os.path.join(dirname, 'camera_param' + '.p'), "rb"))
    mtx, dist, rvecs, tvecs = param[0], param[1], param[2], param[3]
else:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (1920, 1080), None, None)
    dirname = os.path.abspath(__file__ + "/..")
    # pickle.dump([mtx, dist, rvecs, tvecs], open(os.path.join(dirname, 'camera_param' + '.p'), "wb"))


# Calculate reporjection error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error in pixels: {}".format(mean_error/len(objpoints)) )