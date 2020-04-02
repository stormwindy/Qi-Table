import os
from server.vision.camera import Camera
import cv2

camera = Camera(1)
frame = camera.get_image()
dirname = os.path.abspath(__file__ + "/..")
cv2.imwrite(os.path.join(dirname, 'board' + str(50) + '.png'), frame)

