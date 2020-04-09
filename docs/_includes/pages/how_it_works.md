<h1 align="center">How it Works</h1>
<h3 align="center">How does our System Work?</h3>

## System Summary

The Infinitables system consists of mainly 3 parts:

- Physical tables equipped with Arduino-controlled motors.
- A web application that users interact with.
- A server that receives, processes, and sends user commands to the physical tables.

Below is a system diagram that shows how different parts interact with each other:

<p align="center">
  <img width="650" src="static/imgs/system1.png">
</p>

## Tables

The structure of our current product is built from an extremely low weight, medium-density fibreboard. This allowed our engineering team to size the power of the motor down, which drastically reduces the price of the product. Our high efficiency, low cost motors are controlled by a custom motor controller, which is reverse controlled by an Arduino Uno. This allows our tables to arrange themselves into an almost limitless number of configurations and orientations.

Please find one of our table designs below:

<p align="center">

  <img width="325" src="static/imgs/table_drawing.jpg">

  <video width="325" style="height: 100%" controls>
    <source src="static/videos/table_3d.mp4" type="video/mp4">
  </video>

</p>

Table's internal structure allows easy access and maintanance to the user. Table includes 2 motorized wheels and 4 support wheels to keep table in balance, and steer the table in the desired direction. Connection graph of the table with significant components highlighted can be found below. 

<p align="center">
  <img width="650" src="static/imgs/system_diagram_v1.png">
</p>

## Web Application

The users control the system through a web application which allows them to design and edit room layouts (building up a library of reusable setups), execute them and interrupt the operation should any problems arise. It's web based and hosted on the control server, so it can be used both on mobile and desktop, with no installation required!  

The app features a simple interface, built in JavaScript using React, that can be easily used without any previous knowledge of the underlying workings and an intuitive visual editor (using the konva.js library) for layout creation.

## Server

### Vision

The vision module uses an overhead camera to recognize the tables' position and orientation.

<p align="center">
  <img width="550" src="static/imgs/vision1.png">
</p>

The position and orientation information is captured continuously which enables:

- The path finding sub-system to calculate paths for the tables.
- The hardware controller to control the tables' movement.

The vision module is powered by OpenCV.

### Path finding

The path finding module plans collision-free paths for the tables using the position information from the vision module. It enables the tables to form any layout the user wishes. Below is an example where a grid layout is formed from a circular layout.

<p align="center">
  <img width="650" src="https://raw.githubusercontent.com/GavinPHR/Multi-Agent-Path-Finding/master/fig/visualization3.gif">
</p>

The path finding module is powered by a robust hierarchical algorithm with a high-level conflict-based search <a href="https://www.aaai.org/ocs/index.php/AAAI/AAAI12/paper/viewFile/5062/5239">[Sharon et al. 2012]</a> and a low-level space-time A* search. The module is available on <a href="https://github.com/GavinPHR/Multi-Agent-Path-Finding">GitHub</a> and listed on <a href="https://pypi.org/project/cbs-mapf/">PyPI</a>.


### Hardware Controller

Qi's "Infinitables" was developed with a proprietary security protocol including a handshake method. At the initial start-up, the tables will initiate a handshake request with the base computer. This results in the secure storage of a table's identification number in the Electrically Erasable Programmable Read-only Memory, which is safely retained should a power failure occur. The high standard security protocol is merged with each handshake, which ensures a secure communication. To further advance the level of security, the secure keys are regenerated and reassigned periodically.

Qi's intelligent safety sub-systems makes sure that no accidents or damages occur, with the use of a custom-made vision system and the possibility to request the integration of external systems (e.g.: alarm systems)

### Integration

The integration code ties all the software modules together. Below is a common excution flow of the entire system:

<p align="center">
  <img width="550" src="static/imgs/system3.png">
</p>

You can see that integration module serves as a messenger, calling and returning to other modules.

