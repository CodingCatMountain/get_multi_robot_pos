#!/usr/bin/env python
#coding=utf-8
############################################################################
# Description: 读取bag文件提取pos作csv文件
############################################################################
import os,sys
import csv
import rosbag
import rospy
os.chdir(sys.path[0])
bag=rosbag.Bag('Sample_12_10.bag',mode='r')
with open('samples_pos.csv',mode='w') as data_file:
    data_writer=csv.writer(data_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['link_pos_1','link_pos_2','link_pos_3','link_pos_4','link_pos_5','link_pos_6','link_pos_7'])
    # 获取时间范围在/joint_states有效时间内的/iiwa_pos消息(通过rosrun rqt_bag rqt_bag来查看)
    for topic,msg,t in bag.read_messages(topics=['/iiwa_pos']):
        if t.to_sec()>1639136551.935 and t.to_sec()<1639136601.61880:
            p = msg.translation
            data_writer.writerow([[p[0].x,p[0].y,p[0].z],[p[1].x,p[1].y,p[1].z],[p[2].x,p[2].y,p[2].z],\
                                  [p[3].x,p[3].y,p[3].z],[p[4].x,p[4].y,p[4].z],[p[5].x,p[5].y,p[5].z],[p[6].x,p[6].y,p[6].z]])
print("Finished creating csv file!")
bag.close()
