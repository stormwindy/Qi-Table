#!/bin/sh
#Runs on start-up. Sets-up ROS.
source ~/catkkin_ws/src
exec 3< <(roscore)
sed '/started core service [/rosout]/q' <&3 ; cat <&3 &
roslaunch turtlebot3_bringup turtlebot3_robot.launch &
rosrun burger_control burger_control.py
