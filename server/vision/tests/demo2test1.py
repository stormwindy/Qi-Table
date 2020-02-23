from server.vision.camera import Camera
import cv2
import time
c = Camera(1)


def get_pos(num_of_markers, display=False):
    global c
    cap = c.capture
    # Check if the camera is opened and try to get the first frame
    if cap.isOpened():
        frame_captured, frame = cap.read()
    else:
        print('no')
        return
    # Init a dictionary to store positions of AR markers.
    # Format: {marker's ID: marker's location}
    pos = dict()
    taken = 0
    while frame_captured and len(pos) < num_of_markers:  # Break when all markers are recognized.
        taken += 1
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, cv2.aruco.getPredefinedDictionary(0))
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
        print('no')
        return
    print(taken)
    return pos
t1 = time.time()
get_pos(1)
t2 = time.time()
print(t2-t1)