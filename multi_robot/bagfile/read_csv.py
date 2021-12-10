#!/usr/bin/env python
#coding=utf-8
import csv
import pandas as pd
import os,sys
os.chdir(sys.path[0])
df = pd.read_csv('iiwa_sample.csv')
print(df.info())
import ast
print(type(ast.literal_eval(df['link_pos_1'][0])))
#print(df['link_pos_1'][0])