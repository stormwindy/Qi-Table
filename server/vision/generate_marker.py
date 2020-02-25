import cv2


'''
Generate an AR marker and write it to ./markers directory
'''
def generate_marker(id: int = None) -> None:
    # 0 = cv2.aruco.DICT_4X4_50
    dictionary = cv2.aruco.getPredefinedDictionary(0)
    img = cv2.aruco.drawMarker(dictionary, id, 500)
    cv2.imwrite('./markers/marker_{}.png'.format(id), img)
    print("Generated Marker with ID {}".format(id))
    print('Done!')

''' 
E.g. to generate marker with id 5-20:

for i in range(5, 21):
    generate_marker(i)
'''
if __name__ == '__main__':
    generate_marker(2)
