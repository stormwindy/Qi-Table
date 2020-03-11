#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from time import time
import burger_comms

class burger_control:
    def __init__(self):
        self.move_direction = '5'

    def motors_stop(self):
        vel_msg = Twist()
        vel_msg.linear.x=0
        vel_msg.linear.y=0
        vel_msg.linear.z=0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        return vel_msg

    def move_motor(self, command, fwd = 1, ang = 1):
        publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
        mc = Twist()
        if command == self.move_direction:
            return
        publisher.publish(self.motors_stop())

        if command == '1':
            mc.linear.x = -fwd
            self.move_direction = '1'
        elif command == '2':
            mc.linear.x = fwd
            self.move_direction = '2'
        elif command == '3':
            mc.angular.z = ang
            self.move_direction = '3'
        elif command == '4':
            mc.angular.z = -ang
            self.move_direction = '4'
        elif command == '5':
            mc = self.motors_stop()
            self.move_direction = '5'
        publisher.publish(mc)

if __name__ == "__main__":
    rospy.init_node("control_script", anonymous=True)
    control = burger_control()
    comms = burger_comms.Burger_Comms()
    print('initialized')
    while True:
        command = comms.get_payload()
        if command:
            control.move_motor(command)
