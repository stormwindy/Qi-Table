The vision sub-system consists of 3 modules:

 - [generate_marker.py](#generate_markerpy)
 - [camera.py](#camerapy)
 - [room.py](#roompy)
 - [visualizer.py](#visualizerpy)



## generate_marker.py

The module is used to generate AR markers and should be self explanatory to use.


## camera.py 
The module is the main module that carries out the recognition. There are a few pre-requisites you
need to ensure before using this module:

1. The AR markers are placed on a rectangular surface according to specification and are of suitable size.
ONE markers should be placed AT THE CENTER OF the surface.

The size of a marker is currently is 19cm x 19cm.

2. The video capturing device is properly installed, i.e. it recognizes the desired area with enough
resolution. The camera in the SDP arena is 1080p and works well.

To use the Camera class, instantiate with an interface number (an int) that is usually 0 or 1.
DO NOT INSTANTIATE A NEW INSTANCE EVERY TIME WHEN REQUESTING POSITIONS.
This means instantiation should happen in a suitable scope and repeated position requests should
happen inside the scope.

Use the **get_pos(num_of_markers)** to get the position of all markers. Very importantly, you need to specify how many markers there are by passing the num_of_markers argument. get_pos() returns a dictionray with the keys being the marker IDs and values being 4 coordinates corresponding to the 4 corners of the marker, ordered clock-wise from the top left marker.

Despite the exception handling mechanism implemented, two exceptions can still bee raised if things go really wrong, **MarkerRecognitionFailure** and **KeyError**. When these two exceptions are raised, check the camera connection and check that no surfaces is outside the capturing area.

Below is an example use case with two markers to be recognized:
```
c = Camera(1)
pos = c.get_pos(2)
print(pos)
c.release()
```
The output looks like:
```
Vision: start markers recognition.
{2: array([[643., 567.],
           [671., 403.],
           [836., 422.],
           [821., 594.]], dtype=float32), 
 1: array([[423., 538.],
           [474., 390.],
           [623., 396.],
           [592., 560.]], dtype=float32)}
```

## room.py
This module has several drawing functionalities. It can be intialized in two ways:

 - The first takes a picture of the room using the camera, then you will need to manually mark any obstacles with the mouse.
 - The second loads in a picture of the room and a serialized obstacle object. 

In this document, we will focus on how to initialize a room the first way and how 'drawing obstacles with the mouse' works. 

To initilize an object, do:
```
r = Room(0)         
```
A frame will be taken using the camera, and a pop-up canvas will occur. E.g.

<img src="saved/mo1.png" width="400"/>

Remember that obstacles are represented using rectangles, you will need to mark 2 opposite vertices by **Double-Clicking the Left Mouse Button** (every time you double-click, a red circle will appear, not so obvious in the image below):

<img src="saved/mo2.png" width="400"/>

Press 'n' (stands for 'new') when you are finished with marking an obstacle, the edges of the rectangle you just marked will appear, and you can start marking your next obstacle:

<img src="saved/mo3.png" width="400"/>

Once you are done marking, press 'q' to quit. 

The obstacles are stored in a dictionary:
```
 obstacle ID: List of vertices
{0: [[x, y], [   ]],
 1: [[    ], [   ]],
 ..................,
 n: [[    ], [   ]]}
```

You can:

 - use  **show()** to show the frame captured with or without obstacles
 - use **serialize()** to serialize the frame and the obstacle dictionary
 - use **draw_path** to draw a path from vertices

See the module for more details.

## visualizer.py

As the name suggests, this module provides a visualization of:

 - the obstacles
 - the safe/unsafe areas
 - robot's orientation
 - the path planned 

The file can be run directly, assuming that the robot is in the safe area and a valid destination coordinate is set. Below is an example frame:

<img src="saved/visualizer_example.png" width="400"/>

