#!/usr/bin/env python
#coding=utf-8
#############################################################################
# Description: 读取bag文件提取joint_angle作csv文件
#############################################################################
import os,sys
import csv
import rosbag
import rospy

os.chdir(sys.path[0])
bag = rosbag.Bag('Sample_12_10.bag',mode='r')
with open('samples.csv',mode='w') as data_file:
    data_writer=csv.writer(data_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['time','iiwa_joint_1','iiwa_joint_2','iiwa_joint_3','iiwa_joint_4',\
                          'iiwa_joint_5','iiwa_joint_6','iiwa_joint_7'])
    
    # Get all message on the /joint states topic
    for topic,msg,t in bag.read_messages(topics=['/joint_states']):
        #Only write to CSV if the message if for our robot
        if msg.name[0] == "iiwa_joint_1":
            p = msg.position
            data_writer.writerow([t,p[0],p[1],p[2],p[3],p[4],p[5],p[6]])
print("Finished creating csv file!")
bag.close()


