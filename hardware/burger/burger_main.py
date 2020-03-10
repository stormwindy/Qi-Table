import rospy
from geometry_msgs.msg import Twist
from time import time

class burger_control:
    def __init__(self):
        self.move_direction = '5'

    def read_udp_packet():
        pass

    def motors_stop(self) -> Twist:
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
        publisher.publish(self.motors_stop)
        self.move_direction = '5'

        if command == '1':
            mc.linear.x = -fwd
        elif command == '2':
            mc.linear.x = fwd
        elif command == '3':
            mc.angular.z = ang
        elif command == '4':
            mc.angular.z = -ang
        elif command == '5':
            mc = self.motors_stop()
        publisher.publish(mc)