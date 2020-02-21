import cv2
from ar_markers import HammingMarker

'''
Generate an AR marker and write it to current directory
A random id marker is generated if no argument is given
'''
def generate_marker(id: int = None) -> None:
    if id:
        marker = HammingMarker(id=id)
        cv2.imwrite('./markers/marker_{}.png'.format(marker.id), marker.generate_image())
        print("Generated Marker with ID {}".format(marker.id))
    else:
        marker = HammingMarker.generate()
        cv2.imwrite('./markers/marker_{}.png'.format(marker.id), marker.generate_image())
        print("Generated Marker with ID {}".format(marker.id))
    print('Done!')

''' 
E.g. to generate marker with id 5-20:

for i in range(5, 21):
    generate_marker(i)
'''
if __name__ == '__main__':
    generate_marker(5)
