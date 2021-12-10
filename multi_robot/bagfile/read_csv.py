#!/usr/bin/env python
#coding=utf-8
import csv
import pandas as pd
import os,sys
os.chdir(sys.path[0])
df = pd.read_csv('samples_pos.csv')
print(df.to_string)
#print(df.to_excel)
print(df['link_pos_1'])