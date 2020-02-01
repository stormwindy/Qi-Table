import cv2
from ar_markers import detect_markers
import time


class Camera:
    def __init__(self, interface: int):
        self.capture = cv2.VideoCapture(interface)
        # Set the resolution to 1080p
        self.capture.set(3, 1920)
        self.capture.set(4, 1080)

    def get_markers_pos(self, num_of_markers, display: bool = False):
        cap = self.capture
        # Check if the camera is opened and try to get the first frame
        if cap.isOpened():
            frame_captured, frame = cap.read()
        else:
            raise MarkerRecognitionFailure()


        # Init a dictionary to store positions of AR markers
        # Format: {marker's ID: marker's location}
        pos = dict()
        print('Start markers recognition.')
        while frame_captured:
            markers = detect_markers(frame)
            for marker in markers:
                if marker.id not in pos:
                    pos[marker.id] = marker.center
                marker.highlite_marker(frame)

            # Display the feed with marker highlighting
            # if the flag is set to true
            if display:
                cv2.imshow('Test Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                time.sleep(0.01)
            if len(pos) >= num_of_markers:
                break
            frame_captured, frame = cap.read()
        if len(pos) < num_of_markers:
            raise MarkerRecognitionFailure()
        return pos

    def get_pos(self, num_of_tables, display):
        markers_pos = self.get_markers_pos(2*num_of_tables, display)
        pos = dict()
        print(markers_pos)
        for id in markers_pos:
            print(id)
            if id % 2 == 1:
                print(1)
                pos[id] = [markers_pos[id], markers_pos[id + 1]]
        return pos

    def release(self):
        self.capture.release()



class MarkerRecognitionFailure(Exception):
    def __str__(self):
        return 'Method vision.camera.get_markers() failed, make sure ' \
               'the arguments are correct and re-run the method.'



if __name__ == '__main__':
    t1 = time.time()
    c = Camera(1)
    t2 = time.time()
    print(t2 - t1)
    print(c.get_markers_pos(20,True))
    t3 = time.time()
    print(t3 - t2)
    print(c.capture.isOpened())
    c.release()
    print(c.capture.isOpened())
