#!/usr/bin/env python

import rospy
import math
from vrpn_keyboard_control.msg import poses


class crash_checker(object):
    def __init__(self):
        self.car_ips = rospy.get_param('car_ips')
        self.R_safe = rospy.get_param('R_safe')
        self.agent_number =  len(self.car_ips)

    def start(self):
        rospy.init_node('crash_checker', anonymous=True)
        rospy.Subscriber('car_poses_server', poses, self.callback)
        rospy.spin()

    def callback(self, poses_msg):
        position_x = poses_msg.position_x
        position_y = poses_msg.position_y
        crash_list = [False]*self.agent_number
        for idx_a in range(self.agent_number):
            for idx_b in range(self.agent_number):
                if idx_a == idx_b :
                    continue
                distance = (position_x[idx_a]-position_x[idx_b])**2+(position_y[idx_a]-position_y[idx_b])**2
                if distance < (self.R_safe+self.R_safe)**2:
                    crash_list[idx_a] = True
                    break
        rospy.set_param('crash_list', crash_list)


if __name__ == '__main__':
    while True :
        if rospy.get_param('backend_ready'):
            break
    checker = crash_checker()
    checker.start()
