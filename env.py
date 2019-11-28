#!/usr/bin/env python

import rospy
import subprocess
import socket
import threading
import sys
import yaml
import os
import time


HOST = '172.16.0.15'
PORT = 9881
client_list = []
init_flag = 0
LASER_RANGE = 0
ROBOT_LENGTH = 0
agent_num = 0
poses_origin = 0
car_ips = 0
car_targets = 0
init_flag = 0

def init_thread():
    while True:
        if client_list == []:
            continue
        client_address = [sock[1][0] for sock in client_list]
        client_dict = {index: ip for index, ip in zip(range(1, len(client_address)+1), client_address)}
#       print('Existing agents: ' + str(client_dict))
        if len(client_address) != rospy.get_param(agent_num):
            print('Agents Unready! Existing agents: ' + str(client_dict))
        else:
            print('Agents Ready!')
            init_flag = 1
            #break


# system init
def init():
    #read data from yaml
    curPath = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(curPath, "param.yaml")
    yamlfile = open(yamlPath)
    cfg_str = yamlfile.read()
    cfg_dic = yaml.load(cfg_str)
    LASER_RANGE = cfg_dic.get('LASER_RANGE')
    ROBOT_LENGTH = cfg_dic.get('ROBOT_LENGTH')
    agent_num = cfg_dic.get('agent_num')
    poses_origin = cfg_dic.get('poses_origin')
    car_ips = cfg_dic.get('car_ips')
    car_targets = cfg_dic.get('car_targets')
    eps = cfg_dic.get('eps')
    subprocess.Popen("roslaunch vrpn_keyboard_control vrpn_keyboard_control.launch server:=172.16.0.105 >> start_ros.txt", shell=True)
    #os.system('rosparam load param.yaml')
    #os.system('roslaunch vrpn_keyboard_control vrpn_keyboard_control.launch')

    time.sleep(5)

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(10)


    rospy.set_param('LASER_RANGE',LASER_RANGE)
    rospy.set_param('ROBOT_LENGTH',ROBOT_LENGTH)
    rospy.set_param('agent_num',agent_num)
    rospy.set_param('poses_origin',poses_origin)
    rospy.set_param('car_ips',car_ips)
    rospy.set_param('car_targets',car_targets)
    rospy.set_param('eps',eps)
    rospy.set_param('is_reset', False)
    rospy.set_param('is_finish',False)
    rospy.set_param('unset_list', [])
    rospy.set_param('unfinish_list', [])

    t_init = threading.Thread(target=init_thread)
    t_init.start()

#    while True:
#        clientSocket, address = serverSocket.accept()
#        client_list.append([clientSocket, address])

def reset():
    pass


if __name__ == '__main__':
    init()

