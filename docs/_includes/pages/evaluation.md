
<h1 align="center">Evaluation</h1>
<h3 align="center">How Well Does Our System Perform?</h3>


## Evaluation Tests

All the evaluation relating to process makespan were run on a laptop with i7-7700HQ and 16GB of RAM. Vision evaluations were done in a room of size 4m x 3m with a 1080p overhead camera.

### Speed and Accuracy of the Vision Module

It is vital that the vision module can run quickly because it can be called several hundred times in a complete usage cycle. We wrapped the exposed function (which other modules call to get position and orientation information) in a timer, recorded the time between the calling and returning of the function with respect to the number of tables present. Five trials were run for each configuration.

| # of Tables | Time between Calling and Returning (s) |
|:--------:|:------------:|
| 1 | 0.057 | 
| 2 | 0.056 | 
| 3 | 0.056 | 
| 4 | 0.058 | 
| 5 | 0.061 |
| 6 | 0.070 | 
| 7 | 0.087 | 
| 8 | 0.092 |
| 9 | 0.094 |
| 10 | 0.094 |

The results indicate that the vision module is more than fast enough for our system and it will in no way bottleneck our system's performance.

More vital still is that the vision module be as accurate as possible to avoid any chance of collision. We tested vision's accuracy by placing 8 AR tags representing tables in a 4-by-2 formation in different positions and orientations within the operation area. 

Tags were placed equidistant from each other and facing the same direction. We then recorded the position and orientation information returned by vision. In an ideal system, distances between the tables and orientations of the tables should be equal.

The standard error for each of the tests is presented in the table below. On average the standard error is about 0.2° for table orientations and about 0.08cm for distances.

| Test number | Standard error<br>for **orientation** (°) | Standard error<br>for **distance** (cm)|
|:-----------:|:------------------------------------:|:----------------------------------------:|
| 1 | 0.144 | 0.080 |
| 2 | 0.260 | 0.061 |
| 3 | 0.168 | 0.096 |
| 4 | 0.140 | 0.088 |
| 5 | 0.141 | 0.061 |
| 6 | 0.313 | 0.067 |
| 7 | 0.223 | 0.055 |
| 8 | 0.190 | 0.124 |
| 9 | 0.322 | 0.148 |
| 10 | 0.216 | 0.015 |
| 11 | 0.342 | 0.101 |

The results are better than expected as a standard error of 0.2° and 0.08 cm is indistinguishable by eye and small enough to not cause any accidents.

### Speed of the Path Finding Module

The path finding module was tested in simulated environments because we do not have access to any large area yet. The simulated environments are obstacle-free maps of different sizes with different numbers of tables present and a randomised goal layout. We are interested in the time taken to calculate the paths to gauge roughly how long a user would need to wait. 

 | Map Size (grids) | # of Tables | Time Taken to Calculate Paths (s) |
|:-----------:|:-----------------:|:----------------------------------------:|
| 10x10 | 4 | 0.04 |
| 10x10 | 6 | 0.05 |
| 15x15 | 8 | 0.05 |
| 15x15 | 10 | 0.06 |
| 20x20 | 12 | 0.13 |
| 20x20 | 14 | 0.18 |
| 25x25 | 16 | 0.30 |
| 25x25 | 18 | 0.44 |
| 30x30 | 20 | 0.80 |
| 30x30 | 22 | 1.16 |
| 35x35 | 24 | 2.09 |
| 35x35 | 26 | 2.20 |

For perspective, the simulations in the main page have a grid size of 20x30.

We can see that the time it takes increases faster and faster as the number of agent increases and the maps becomes larger. The time is acceptable for our prototype system at the moment but we will improve upon this results.


### User Tests

While the current global circumstances have made testing the whole integrated system impossible, presenting the web app to a few testers revealed a number of places for improvement. 

Firstly, most users had trouble realising that rotation of tables in the editor was possible or figuring out how to perform it once they had learned about it. This has been alleviated by making the rotation handle appear when tables are dragged around and not just when clicked on, so that users will be more likely to be exposed to it and investigate. The handle was also changed from a square to a circular arrow, similar to ones in slideshow editors, to make its intended functionality more intuitive.  

In addition, to allow for very precise alignment of tables a few collision prevention methods (i.e. what happens when a user puts a table on top of another one) were considered, including snapping back to the original location, and not allowing tables to be dragged over one another altogether. The one that users found most intuitive was snapping back to the closest non-overlapping location when dragging is finished, using an implementation of the Separating Axis Theorem. This has the benefit of making close alignment of tables very simple.



## Main Areas of Improvement

The path finding module needs more work to be viable in much more complex settings. The problems and the solutions are as follows:

-  The module's parallelization is currently done by multi-processing only. But we can and should take advantage of threading because some jobs are too small for a new process.
- The module is currently written in Python and a part of it is non-optimized native Python. This definitely impacts the performance and we are considering porting the module to a low level language instead.
