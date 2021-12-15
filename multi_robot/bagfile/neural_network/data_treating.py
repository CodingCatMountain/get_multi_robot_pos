#!/usr/bin/env python3
#coding=utf-8
# import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error
import joblib
import collections

# import the csv file
import os,sys
os.chdir(sys.path[0])
df = pd.read_csv('../iiwa_sample.csv')