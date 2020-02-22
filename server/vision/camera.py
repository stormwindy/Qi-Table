import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../..'))
import cv2
import numpy as np
import time
from typing import Dict, Tuple

'''
See README for usage.
'''
class Camera:

    '''
    interface should be a number specifying the
    camera to be used. On UNIX for example, interface
    should be 0 if your device is /dev/video0.
    '''
    def __init__(self, interface: int):
        self.capture = cv2.VideoCapture(interface)
        # Set the resolution to 1080p
        self.capture.set(3, 1920)
        self.capture.set(4, 1080)
        # 0 = cv2.aruco.DICT_4X4_50
        self.dictionary = cv2.aruco.getPredefinedDictionary(0)

    '''
    Do NOT use this method outside this module, use the get_pos() method instead.
    For testing, set the display flag to True to display a live video feed.
    '''
    def get_pos(self, num_of_markers: int, display: bool = False) -> Dict[int, np.ndarray]:
        cap = self.capture
        # Check if the camera is opened and try to get the first frame
        if cap.isOpened():
            frame_captured, frame = cap.read()
        else:
            raise MarkerRecognitionFailure()

        # Init a dictionary to store positions of AR markers.
        # Format: {marker's ID: marker's location}
        pos = dict()
        print('Vision: start markers recognition.')
        while frame_captured and len(pos) < num_of_markers:  # Break when all markers are recognized.
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, self.dictionary)
            if ids is not None:
                for i in range(len(ids)):
                    pos[ids[i][0]] = corners[i][0]

            # Display the feed with marker highlighting
            # if the display flag is set to true.
            if display:
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                cv2.imshow('Test Frame', frame)
                # Break when 'q' is pressed (& 0xFF required for 64-bit architecture)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            frame_captured, frame = cap.read()

        if len(pos) < num_of_markers:
            raise MarkerRecognitionFailure()
        return pos

    # '''
    # Use this method to get the positions of the surfaces.
    # '''
    # def get_pos(self, num_of_surfaces: int, display: bool = False) -> Dict[int, Tuple[Tuple[int], Tuple[int]]]:
    #     # Recognize marker positions repeatedly, stop when:
    #     #   1. a successful recognition is achieved
    #     #   2. 5 iterations passed and an exception is raised
    #     markers_pos = None
    #     counter = 5
    #     while counter:
    #         try:
    #             markers_pos = self.__markers_pos(2*num_of_surfaces, display)
    #             break
    #         except MarkerRecognitionFailure:
    #             counter -= 1
    #             continue
    #     if markers_pos is None:
    #         raise MarkerRecognitionFailure()
    #
    #     # Group marker together to to form a table,
    #     # every table is specified by two markers.
    #     pos = dict()
    #     for id in markers_pos:
    #         if id % 2 == 1:
    #             try:
    #                 pos[id] = (markers_pos[id], markers_pos[id + 1])
    #             except KeyError as e:
    #                 print('vision.camera.get_pos(),'
    #                       'check markers ID correctness.')
    #                 raise e
    #     return pos

    '''
    Return one frame from the camera feed
    '''
    def get_image(self) -> np.ndarray:
        cap = self.capture
        for _ in range(5):
            frame_captured, frame = cap.read()
        if frame_captured:
            return frame
        else:
            return np.nan

    # Release the video capture.
    def release(self):
        self.capture.release()

'''
Custom exception to catch.
'''
class MarkerRecognitionFailure(Exception):
    def __str__(self):
        return 'Method vision.camera.get_markers() failed, make sure ' \
               'the arguments are correct and re-run the method.'


'''
Test run.
'''
if __name__ == '__main__':
    t1 = time.time()
    c = Camera(0)
    t2 = time.time()
    print(t2 - t1)
    print(c.get_pos(2, True))
    t3 = time.time()
    print(t3 - t2)
    print(c.capture.isOpened())
    c.release()
    print(c.capture.isOpened())
