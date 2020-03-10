import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../..'))
import cv2
from server.vision.camera import Camera
import time
from collections import defaultdict
import pickle
import numpy as np

'''
See README for more info.
'''
class Room:

    '''
    Argument param should be either an int or a str, more details below.
    '''
    def __init__(self, param):
        # int param should be a video interface, normally 0 or 1
        if isinstance(param, int):
            camera = Camera(param)
            # fram_orig is the original frame taken, and will remain unmodified
            self.frame_orig = camera.get_image()
            if self.frame_orig is np.nan:
                raise RuntimeError('vision: camera was not initialized properly.')
            # frame_obst will be drawn on
            self.frame_obst = self.frame_orig.copy()
            # obsts: dict stores all the obstcles
            self.obsts = None
            self.__mark_obstacles()
            camera.release()
        # str param should be file names to read in
        elif isinstance(param, str):
            dirname = os.path.abspath(__file__ + "/..")
            self.frame_orig = cv2.imread(os.path.join(dirname, 'saved', param +'.png'))
            self.obsts = pickle.load(open(os.path.join(dirname, 'saved', param +'.p'), "rb"))
            self.frame_obst = self.frame_orig.copy()
            # Uncomment the line below to draw polygons instead
            # self.draw_poly(np.array([np.array(v) for v in self.obsts.values()]))
            self.draw_rect(np.array([np.array(v) for v in self.obsts.values()]))
        else:
            raise TypeError('vision.room.__init__: please pass either an int or a str')

    '''
    Draw a rectangles given a list of opposite vertices
    '''
    def draw_rect(self, pts_arr: np.ndarray) -> None:
        for pts in pts_arr:
            cv2.rectangle(self.frame_obst, tuple(pts[0]), tuple(pts[1]), (0, 0, 255), thickness=3)

    '''
    Draw polygons from vertices' locations - numpy 3d array:
    [[[x, y],..., [   ]],  <- polygon1
     [[    ],..., [   ]]]  <- polygon2
    '''
    def draw_poly(self, vertices: np.ndarray) -> None:
        cv2.polylines(self.frame_obst, vertices, True, (0, 0, 255), thickness=3)

    '''
    Draw path from nodes' locations - numpy 3d array:
    [[[x, y],..., [   ]],  <- path1
     [[    ],..., [   ]]]  <- path2
    '''
    def draw_path(self, vertices: np.ndarray) -> None:
        cv2.polylines(self.frame_obst, vertices, False, (0, 255, 0), thickness=3)

    '''
    A window will pop up for manual obstacle marking.
    Select obstacle vertices one by one by double-clicking 
    mouse left button. Press 'n' to start mark a new obstacle.
    Once completed, press 'q' to quit.
    The markings is visualized in real time.
    '''
    def __mark_obstacles(self) -> None:
        obsts = defaultdict(list)
        obst_index = 0

        # Mouse callback function
        def draw_vertex(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDBLCLK:
                cv2.circle(self.frame_obst, (x, y), 3, (0, 0, 255))
                obsts[obst_index].append([x, y])

        cv2.namedWindow('mark_obst')
        cv2.setMouseCallback('mark_obst', draw_vertex)
        while True:
            cv2.imshow('mark_obst', self.frame_obst)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('n'):
                # Uncomment the line below if polygons are wanted
                # self.draw_poly(np.array([obsts[obst_index]]))
                self.draw_rect(np.array([obsts[obst_index]]))
                obst_index += 1
            elif k == ord('q'):
                break
        self.obsts = obsts
        cv2.destroyAllWindows()

    '''
    Serialize and save the frames and the obstacles.
    '''
    def serialize(self, index=0) -> None:
        dirname = os.path.abspath(__file__ + "/..")
        cv2.imwrite(os.path.join(dirname, 'saved', 'room' + str(index) + '.png'), self.frame_orig)
        cv2.imwrite(os.path.join(dirname, 'saved', 'room' + str(index) + '_obst.png'), self.frame_obst)
        pickle.dump(self.obsts, open(os.path.join(dirname, 'saved/room' + str(index) + '.p'), "wb"))

    '''
    Show the frame (turn on with_obstacles flag to show with obstacles)
    Press 'q' to exit, press 's' to save & exit.
    '''
    def show(self, with_obstacles: bool = False):
        if not with_obstacles:
            cv2.imshow('frame_orig', self.frame_orig)
        else:
            cv2.imshow('frame_obst', self.frame_obst)
        k = cv2.waitKey(0) & 0xFF  # '& 0xFF' for 64-bit compatibility
        if k == ord('q'):
            cv2.destroyAllWindows()
        elif k == ord('s'):
            self.serialize()
            cv2.destroyAllWindows()

'''
Test code.
'''
if __name__ == '__main__':
    t1 = time.time()
    # r = Room('room0')  # Load saved room and obstacles
    r = Room(1)        # Take a picture of the room and mark obstacles manually
    t2 = time.time()
    # r.draw_path(np.array([[[500,100],[500,600], [600,600]]]))
    print(t2-t1)
    r.show(True)
    t3 = time.time()
    print(t3-t2)
