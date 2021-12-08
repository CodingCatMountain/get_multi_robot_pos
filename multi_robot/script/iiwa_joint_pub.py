#!/usr/bin/env python
#coding=utf-8
import rospy
import sys
import os,sys
os.chdir(sys.path[0])
import numpy as np
from sensor_msgs.msg import JointState

# 导入joint_samples.npy
joint_samples=np.load('joint_samples.npy')

IIWA_JOINT_NAME = ['iiwa_joint_1','iiwa_joint_2','iiwa_joint_3','iiwa_joint_4','iiwa_joint_5','iiwa_joint_6','iiwa_joint_7']

class iiwa_joint_publisher():
    def __init__(self):
        rospy.init_node("iiwa_joint_state_publisher")
        self.__msg = JointState()
        self.__msg.name = IIWA_JOINT_NAME
        self.__publisher = rospy.Publisher("/joint_states",JointState,queue_size=10)
        self.__rate=rospy.Rate(10)
        self.__pos=[]
    
    def publish(self):
            for i in range(joint_samples.shape[0]): #遍历一百组数据
                for j in range(joint_samples.shape[1]): #拿出每组数据传入pos中
                    self.__pos.append(joint_samples[i][j])
                # 向消息中加入时间戳
                self.__msg.header.stamp = rospy.Time.now()
                self.__msg.name = IIWA_JOINT_NAME
                self.__msg.position = self.__pos
                self.__publisher.publish(self.__msg)
                self.__rate.sleep()
                # 清空pos栏
                self.__pos=[]
            pass


if __name__=='__main__':
    try:
        iiwa_publisher=iiwa_joint_publisher()
        iiwa_publisher.publish()
    except rospy.ROSInterruptException:
        pass

    