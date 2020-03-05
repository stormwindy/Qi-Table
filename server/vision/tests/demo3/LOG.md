RAW:
floor area 280x360cm (not whole frame, left and right was tables)
so 1080x(some dim) px

reprojection error: 9.79px ?= 2.59cm diff

test2:
10 markers placed in the middle of the frame horizontally, each with center 25cm away from each other
\[106.764 105.507 106.011 102.005 110.26  106.753 107.751 107.011 107.755\]  avg = 106.646

***** vertically ***
\[106.257 106.269 106.764 106.007 105.255 106.005 104.501 103.251 103.5  \] avg = 105.312 px

***** diagonally ***
\[105.738 106.05  107.69  108.043 106.776 106.423 107.129 105.011 105.738\] avg = 106.510 px


3-by-3 (tight) formation, all 90 deg see testFrame4
\[90.    89.17  90.    90.    90.    89.17  88.315 87.474 89.17 \] avg = 89.255 deg

3-by-3 (loose) formation, all 90 deg see testFrame7
\[87.474 89.17  90.    87.436 88.34  90.    87.436 89.145 90.   \] avg = 88.77784402717273
pattern left to right

PROCESSED:
dist
106.156px/25cm   var=2.575, std=1.605 
4.246px/cm ~ 1.605/4.246 = 0.378cm error / every 25cm

deg
89.017 var=0.977 std=0.988
expect about 2 degrees of difference at most

reprojection error: 9.79px, quite high, checkerboard not rigid/big enough, camera distortion quite bad


