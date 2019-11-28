#!/usr/bin/env python
#coding=UTF-8

import rospy
import copy
from vrpn_keyboard_control.srv import *
from vrpn_keyboard_control.msg import vels
class set_action_server:
    def __init__(self):
        self.agent_num = rospy.get_param('agent_num')
        self.linear_recv = []
        self.angular_recv = []
        self.seq = 0
        self.linear = []
        self.angular = []
        for i in range(self.agent_num):
            self.linear_recv.append(0)
            self.angular_recv.append(0)
            self.linear.append(0)
            self.angular.append(0)
    def handle_funtion(self, set_action):
        self.seq = self.seq + 1
        self.linear_recv = copy.deepcopy(set_action.linear_action_list)
        self.angular_recv = copy.deepcopy(set_action.angular_action_list)
        enable = copy.deepcopy(set_action.enable_list)
        for i in range(self.agent_num):
            if enable[i] == True:
                self.linear[i] = self.linear_recv[i]
                self.angular[i] = self.angular_recv[i]
                rospy.loginfo(str(self.linear[i])+','+str(self.angular[i]))
        pub = rospy.Publisher('car_vels_server', vels, queue_size = 10)
        vels_msg = vels()
        vels_msg.seq = self.seq
        vels_msg.vel_linear = self.linear
        vels_msg.vel_angular = self.angular
        pub.publish(vels_msg)
        rospy.loginfo(self.seq)
        return set_actionResponse(True)
        
    def sas(self):
        rospy.set_param('is_setaction', 1)
        rospy.init_node('set_action_server', anonymous=True)
        srv = rospy.Service('set_action', set_action, self.handle_funtion)
        rospy.spin()


if __name__ == '__main__':
    while True :
        if rospy.get_param('backend_ready'):
            break
    s = set_action_server()
    s.sas()
        