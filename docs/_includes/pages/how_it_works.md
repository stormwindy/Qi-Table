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

## Methods

Qi's Infinitables was developed with a proprietary security protocol including a handshake method. At the initial startup, the tables will initiate a handshake request with the base computer. This will result in the secure storage of a table identification in the Electrically Erasable Programmable Read-only Memory, which allows a seamless operation at a power failure scenario. The high standard security protocol is merged with each handshake, which ensures a secure communication. To further advance the level of security, the secure keys are regenerated and reassigned periodically.

Qi's intelligent safety sub-systems makes sure that no accidents or damages happens, with the use of a custom-made vision system and a possibility to request the integration of external systems (e.g.: alarm systems)

### System Diagrams

You should include images (where available) which illustrate the methods you used, how the system works etc.

This can include system diagrams, images of your system in certain states etc.
