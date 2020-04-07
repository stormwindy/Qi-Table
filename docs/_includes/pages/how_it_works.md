<h1 align="center">How it Works</h1>
<h3 align="center">How does our System Work?</h3>

## System Summary

The Infinitables system consists of mainly 3 parts:

- Physical tables equipped with Arduino-controlled motors.
- A web application that users interact with.
- A server that recieves, processes, and sends user commands to the physical tables.

Below is a system diagram that shows how different parts interact with each other:

<p align="center">
  <img width="650" src="static/imgs/system1.png">
</p>

## Tables

The structure of our current product is built from an extremely low weight medium-density fibreboard. This allowed our engineering team to size the power of the motor down, which drastically reduces the price of the product. Our high efficiency, low cost motors are controlled by a costume motor controller, which in reverse controlled by an Arduino Uno. One of the many pros of choosing Qi's Infinitables is the infinite dimension selection, as for our partners, we can manufacture uniquely sized tables.

Please find one of our table designs below:

<p align="center">

  <img width="325" src="static/imgs/table_drawing.jpg">

  <video width="325" style="height: 100%" controls>
    <source src="static/videos/table_3d.mp4" type="video/mp4">
  </video>

</p>

## Web Application

what framework? how to use?

## Server

### Vision

The vision module uses an overhead camera to recognize the tables' position and orientation.

<p align="center">
  <img width="650" src="static/imgs/vision1.png">
</p>

The position and orientation information is captured continuously which enables:

- The path finding sub-system to calculate paths for the tables.
- The hardware controller to control the tables' movement.

The vision module is powered by OpenCV.

### Path finding

The path finding module plans collision-free paths for the tables using the position information from the vision module. It enables the tables to form any layout the user wishes. Below is an example where a grid layout is formed from a circular layout.

<p align="center">
  <img width="650" src="https://raw.githubusercontent.com/GavinPHR/Multi-Agent-Path-Finding/master/fig/visualization2.gif">
</p>

The path finding module is powered by a robust hierarchical algorithm with a high-level conflict-based search <a href="https://www.aaai.org/ocs/index.php/AAAI/AAAI12/paper/viewFile/5062/5239">[Sharon et al. 2012]</a> and a low-level space-time A* search.


### Hardware Controller

Qi's Infinitables was developed with a proprietary security protocol including a handshake method. At the initial startup, the tables will initiate a handshake request with the base computer. This will result in the secure storage of a table identification in the Electrically Erasable Programmable Read-only Memory, which allows a seamless operation at a power failure scenario. The high standard security protocol is merged with each handshake, which ensures a secure communication. To further advance the level of security, the secure keys are regenerated and reassigned periodically.

Qi's intelligent safety sub-systems makes sure that no accidents or damages happens, with the use of a custom-made vision system and a possibility to request the integration of external systems (e.g.: alarm systems)

### Integration

The integration code ties all the software modules together. Below is a common excution flow of the entire system:

<p align="center">
  <img width="550" src="static/imgs/system2.png">
</p>

You can see that integration serves as a messenger that calls and returns to other modules.

