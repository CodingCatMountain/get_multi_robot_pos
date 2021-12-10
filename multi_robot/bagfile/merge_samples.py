#!/usr/bin/env python
#coding=utf-8
import os,sys
import csv

from pandas.core.algorithms import mode
import rosbag
import rospy
os.chdir(sys.path[0])
############################################################################
# Description: 合并Samples_pos.csv 与 Sample.csv
############################################################################
import pandas as pd
joint_sample=pd.read_csv('samples.csv')
pos_sample=pd.read_csv('samples_pos.csv')
_index = []
for i in range(0,497):
    _index.append(i)

final_sample=pd.merge(joint_sample,pos_sample,how='inner',left_index=True,right_index=True)
print(final_sample.info())
final_sample.to_csv('iiwa_sample.csv',mode='a+')
