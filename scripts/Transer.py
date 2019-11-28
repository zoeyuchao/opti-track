#!/usr/bin/env python
#coding=UTF-8

import rospy
from vrpn_keyboard_control.srv import *
from vrpn_keyboard_control.msg import poses

class Trans:
    def __init__(self):
        self.x = []
        self.y = []
        self.yaw = []
        self.target_x = []
        self.target_y = []
    def tr(self):
        rospy.init_node('Transer', anonymous = True)
        srv = rospy.Service('position', position, self.handle_function)   #定义程序的Server端
        rospy.Subscriber('car_poses_server', poses, self.callback)
        rospy.loginfo('Ready to handle the request:')
        rospy.spin()
    def callback(self, poses):
        self.x = poses.position_x
        self.y = poses.position_y
        self.yaw = poses.position_yaw
        self.target_x = poses.target_x
        self.target_y = poses.target_y
        #rospy.set_param('run_callback', 1)
        #print('class_callback', self.l)
    def handle_function(self, req):
        #rospy.set_param('obs_x', self.x)
        #print(self.l)
        #print('class_handle_function is working')
        return positionResponse(self.x, self.y, self.yaw, self.target_x, self.target_y)

#def callback(poses):
    #l = poses
    #srv = rospy.Service('greetings', Greeting, handle_function, memory)
    #print('callback ', l)

#def server():
    #rospy.init_node('greeting_pyserver', anonymous = True)
    #srv = rospy.Service('greetings', Greetings, handle_function)   #定义程序的Server端
    #rospy.loginfo('Ready to handle the request:')
    #rospy.spin()

#def handle_function(req):
    #print('handle_function is working')
    #s = req.req + 1
    #l.append(s)
    #l.append(s+1)
	# 返回一个Service_demoResponse实例化对象，其实就是返回一个response的对象，其包含的内容为我们再Service_demo.srv中定义的
    # response部分的内容，我们定义了一个string类型的变量，因此，此处实例化时传入字符串即可
    #return GreetingsResponse(l)

# 如果单独运行此文件，则将上面定义的server_srv作为主函数运行
if __name__ == '__main__':
    t = Trans()
    t.tr()
    #rospy.init_node('greeting_pyserver', anonymous = True)
    #srv = rospy.Service('greetings', Greetings, handle_function)   #定义程序的Server端
    #rospy.Subscriber('poses', poses, callback)
    #rospy.loginfo('Ready to handle the request:')
    #rospy.spin()