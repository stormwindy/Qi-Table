import cv2
from ar_markers import detect_markers

def get_markers(numOfMarkers):
    print('Press "q" to quit')
    capture = cv2.VideoCapture(1)

    if capture.isOpened():  # try to get the first frame
        frame_captured, frame = capture.read()
    else:
        frame_captured = False

    count = 0
    ids = set()
    detectedMarkers = []

    while frame_captured:
        markers = detect_markers(frame)
        for marker in markers:
            if marker.id not in ids:
                ids.add(marker.id)
                detectedMarkers.append(marker)
                count += 1
            marker.highlite_marker(frame)
        cv2.imshow('Test Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_captured, frame = capture.read()
        if count == numOfMarkers:
            break

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()
    return detectedMarkers

markers = get_markers(10)
for marker in markers:
    print(marker.id, marker.contours)

