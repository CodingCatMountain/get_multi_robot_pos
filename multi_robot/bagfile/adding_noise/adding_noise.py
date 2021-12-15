#!/usr/bin/env python3
#coding=utf-8
import pandas as pd
import numpy as np
import os,sys
import ast
os.chdir(sys.path[0])

def add_noise(pos):
    '''
        param: pos 从csv中读取的连杆位置的数据，List类型
        func : 向pos中添加正态分布的噪声,均值为0，标准差为error1
    '''
    # 转换为ndarray对象
    pos_array=np.array(pos)
    pos_error = 0.1
    #pos_noise = pos_error*np.random.normal(size=pos_array.size)
    #for i in range(len(pos_noise)):
        #if pos_noise[i]>0.1 or pos_noise[i]<0.1:
            #pos_noise[i] = pos_error*np.random.normal()
    pos_noise=[]
    # 添加[-0.1,0.1]之间以正态分布获得的noise值
    for i in range(0,3):
        pos_noise_ = pos_error*np.random.normal()
        while(pos_noise_<-0.1 or pos_noise_>0.1):
            pos_noise_ = pos_error*np.random.normal()
        pos_noise.append(pos_noise_)

    
    pos_array = pos_array+pos_noise
    return list(pos_array)



if __name__== "__main__":

    # read the csv data
    df=pd.read_csv(r'../iiwa_sample.csv')

    # By df.itertuples() 迭代遍历每一行
    for row in df.itertuples():

        # 读取每一行中对应列的数据
        Link_Pos_1 = ast.literal_eval(row.link_pos_1)
        Link_Pos_2 = ast.literal_eval(row.link_pos_2)
        Link_Pos_3 = ast.literal_eval(row.link_pos_3)
        Link_Pos_4 = ast.literal_eval(row.link_pos_4)
        Link_Pos_5 = ast.literal_eval(row.link_pos_5)
        Link_Pos_6 = ast.literal_eval(row.link_pos_6)
        Link_Pos_7 = ast.literal_eval(row.link_pos_7)
        
        #print("originate pos:")
        #print(Link_Pos_2)
        #print("after adding noise:")
        #Link_Pos_2 = add_noise(Link_Pos_2)
        #print(Link_Pos_2)
        #break
        Link_Pos_1 = add_noise(Link_Pos_1)
        Link_Pos_2 = add_noise(Link_Pos_2)
        Link_Pos_3 = add_noise(Link_Pos_3)
        Link_Pos_4 = add_noise(Link_Pos_4)
        Link_Pos_5 = add_noise(Link_Pos_5)
        Link_Pos_6 = add_noise(Link_Pos_6)
        Link_Pos_7 = add_noise(Link_Pos_7)

        # 将加有噪声的数据替换原来的数据
        df.loc[row.Index,('link_pos_1')]=str(Link_Pos_1)
        df.loc[row.Index,('link_pos_2')]=str(Link_Pos_2)
        df.loc[row.Index,('link_pos_3')]=str(Link_Pos_3)
        df.loc[row.Index,('link_pos_4')]=str(Link_Pos_4)
        df.loc[row.Index,('link_pos_5')]=str(Link_Pos_5)
        df.loc[row.Index,('link_pos_6')]=str(Link_Pos_6)
        df.loc[row.Index,('link_pos_7')]=str(Link_Pos_7)

    df.to_csv(r'../iiwa_samples_with_noise.csv')

    
    
    
