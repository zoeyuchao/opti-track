#!/usr/bin/env python

import rospy
import math
import time
import copy
from vrpn_keyboard_control.msg import poses







class controller(object):
    def __init__(self):
        self.car_ips = rospy.get_param('car_ips')
        self.R_reach = rospy.get_param('R_reach')
        self.agent_number =  len(self.car_ips)

    def start(self):
        rospy.init_node('controller',anonymous=True)
        rospy.Subscriber('car_poses_server', poses, self.callback)
        rospy.spin()

    def callback(self,poses_msg):
        poses_origin = rospy.get_param('poses_origin')
        target_x = poses_msg.target_x
        target_y = poses_msg.target_y
        position_yaw = poses_msg.position_yaw
        position_x = poses_msg.position_x
        position_y = poses_msg.position_y
        set_state_list = [False]*self.agent_number
        reach_state_list = [False]*self.agent_number
        unset_list = []
        unfinish_list = []
        for idx_a in range(self.agent_number):
            set_distance = (poses_origin[idx_a][0] - position_x[idx_a])**2 + (poses_origin[idx_a][1] - position_y[idx_a])**2
            angle_dist = (math.cos(poses_origin[idx_a][2] - position_yaw[idx_a])-1)**2
            if set_distance < self.R_reach**2  and angle_dist<2e-5:
                set_state_list[idx_a] = True
            else:
                unset_list.append(self.car_ips[idx_a])

            target_distance = (target_x[idx_a] - position_x[idx_a])**2 + (target_y[idx_a] - position_y[idx_a])**2
            if target_distance < self.R_reach**2:
                reach_state_list[idx_a] = True
            else:
                unfinish_list.append(self.car_ips[idx_a])

        rospy.set_param('is_reset', len(unset_list) == 0)
        rospy.set_param('is_finish',len(unfinish_list) == 0)
        rospy.set_param('reach_list',reach_state_list)
        rospy.set_param('unset_list', unset_list)
        rospy.set_param('unfinish_list', unfinish_list)



def callback(poses):
    #R_safe = rospy.get_param('R_safe')
    R_reach = rospy.get_param('R_reach')
    car_ips = rospy.get_param('car_ips')
    unset_list = copy.deepcopy(car_ips)
    unfinish_list = copy.deepcopy(car_ips)
    poses_origin = rospy.get_param('poses_origin')
    target_x = poses.target_x
    target_y = poses.target_y
    position_x = poses.position_x
    position_y = poses.position_y
    for i in range(0, len(car_ips)):
        origin_distance = math.sqrt((poses_origin[i][0] - position_x[i])*(poses_origin[i][0] - position_x[i])+(poses_origin[i][1] - position_y[i])*(poses_origin[i][1] - position_y[i]))
        #rospy.set_param('o_d', origin_distance)
        target_distance = math.sqrt((target_x[i] - position_x[i])*(target_x[i] - position_x[i])+(target_y[i] - position_y[i])*(target_y[i] - position_y[i]))
        rospy.logdebug(str(i)+" init : "+str(poses_origin[i])+" pos : "+str(position_x[i])+str(position_y[i]))
        if origin_distance > R_reach:
            if not(car_ips[i] in unset_list):
                unset_list.append(car_ips[i])
        else:
            if car_ips[i] in unset_list :
                unset_list.remove(car_ips[i])
        if target_distance > R_reach:
            if not(car_ips[i] in unfinish_list):
                unfinish_list.append(car_ips[i])
        else:
            if car_ips[i] in unfinish_list :
                unfinish_list.remove(car_ips[i])
    if unset_list == []:
        rospy.set_param('is_reset', True)
    else:
        rospy.set_param('is_reset', False)
    if unfinish_list == []:
        rospy.set_param('is_finish', True)
    else:
        rospy.set_param('is_finish', False)
    rospy.set_param('unset_list', unset_list)
    rospy.set_param('unfinish_list', unfinish_list)




if __name__ == '__main__':
    while True :
        if rospy.get_param('backend_ready'):
            break
    c = controller()
    c.start()
