#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import PoseStamped
from vrpn_keyboard_control.msg import poses
from vrpn_keyboard_control.msg import pose
#import PyKDL as kdl
import threading

agent_num = 2


def q2euler(x,y,z,w):
    y = 2*math.atan2(y,w)
    r = math.atan2(2*(w*x+y*z),1-2*(x*x+y*y))
    p = 0
    # p = math.asin(2*(w*y-z*z))
    #y = math.atan2(2*(w*z+x*y),1-2*(z*z+y*y))
    return y,r,p

def callback(msg):
    global rigidbody_poses
    global string
    seq = msg.header.seq
    x = msg.pose.position.x
    y = msg.pose.position.y
    z = msg.pose.position.z
    qx = msg.pose.orientation.x
    qy = msg.pose.orientation.y
    qz = msg.pose.orientation.z
    qw = msg.pose.orientation.w

#    rotation_matrix = 

    #yaw, pitch, roll = kdl.Rotation.Quaternion(qx, qy, qz, qw).GetEulerZYX()

    yaw, roll, pitch = q2euler(qx,qy,qz,qw)

    if(yaw > 2*math.pi):
        yaw = yaw - 2 * math.pi
    elif(yaw <= 0):#math.pi):
        yaw = yaw + 2 * math.pi
    
    roll = roll/math.pi*180

    pitch = pitch/math.pi*180
    
    string = ("mid:%d;x:%d;y:%d;z:%d;mpry:%d;pitch:%d;roll:%d;yaw:%d;"%(1,x,y,z,1,pitch,roll,yaw))

    # rospy.loginfo("RigidBody0%d[coordinate]: Header seq = %d; Position x = %f, y = %f, z = %f; Orientation roll = %f, pitch = %f, yaw = %f.", car_index+1, seq, x, y, z, roll, pitch, yaw)

def ros_thread():
    rospy.Subscriber('/vrpn_client_node/Car01/pose', PoseStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('vrpn_pose', anonymous=True)
    string = 0
    rospy.set_param('string', string)
    t_ros = threading.Thread(target=ros_thread)
    t_ros.start()
    pub = rospy.Publisher('car_poses_server', pose, queue_size = 10)
    rospy.set_param('string', string)
    rate = rospy.Rate(50)
    seq = 0
    while not rospy.is_shutdown():
        # print(pose_msg)
        # rospy.loginfo("car_poses: seq = %d, position_x = %s, position_y = %s, position_yaw = %s, target_x = %s, target_y = %s.", pose_msg.seq, str(pose_msg.position_x), 
            # str(pose_msg.position_y), str(pose_msg.position_yaw), str(pose_msg.target_x), str(pose_msg.target_y))     
        pub.publish(string)
        seq += 1
        rate.sleep()
