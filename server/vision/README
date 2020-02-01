See the <a href="https://github.com/DebVortex/python-ar-markers" target="_blank">ar-markers GitHub</a> for a more complete understanding.

The vision sub-system consists of two modules:

 - generate_marker.py
 - camera.py

generate_marker.py is used to generate AR markers and should be self explanatory to use.

camera.py is the main module that carries out the recognition. There are a few pre-requisites you
need to ensure before using this module:

1. The AR markers are placed on a rectangular surface according to specification and are of suitable size.
Two markers should be placed on each surface like so:
<img src="markers/table1.png" alt="Table with ID 1" width="200"/>
The left marker has ID 1 and the right marker has ID 2. The whole surface is identified with the ID of
the left marker, i.e. ID 1. The left marker ID should always be odd and the corresponding right marker
should have an ID value 1 more than the left.
A suitable size is hard to define, but in the SDP arena, the size of each marker should be roughly 6cm x 6cm.

2. The video capturing device is properly installed, i.e. it recognizes the desired area with enough
resolution. The camera in the SDP arena is 1080p and works well.

To use the Camera class, instantiate with an interface number (an int) that is usually 0 or 1.
DO NOT INSTANTIATE A NEW INSTANCE EVERY TIME WHEN REQUESTING POSITIONS.
This means instantiation should happen in a suitable scope and repeated position requests should
happen inside the scope.

Use the **get_pos(num_of_surfaces)** to get the position of all surfaces. Very importantly, you need to specify
how many surfaces there are by passing the num_of_surfaces argument. get_pos() returns a dictionray with the keys being the surface IDs and values being a pair of coordinates specifying the left and right coordinates of
the surface.

Despite the exception handling mechanism implemented, two exceptions can still bee raised if things go really wrong, **MarkerRecognitionFailure** and **KeyError**. When these two exceptions are raised, check the camera connection and check that no surfaces is outside the capturing area.

Below is an example use case with two surfaces to be recognized:
```
c = Camera(1)
pos = c.get_pos(2)
print(pos)
c.release()
```
 The output looks like:
 ```
 Vision: start markers recognition.
{3: ((555, 674), (999, 611)), 1: ((397, 861), (163, 484))}
```