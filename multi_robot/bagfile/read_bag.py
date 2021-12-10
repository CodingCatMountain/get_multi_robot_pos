#!/usr/bin/env python
#coding=utf-8
import os,sys
import ros
os.chdir(sys.path[0])
import rosbag
bag = rosbag.Bag('./Sample_12_10.bag')
#import subprocess,yaml
#info_dict=yaml.load(bag._get_yaml_info(),Loader=yaml.FullLoader)

for topic,msg,t in bag.read_messages(topics=['/iiwa_pos']):
    print(t.to_sec())
    print(msg.translation)
    print("============")


