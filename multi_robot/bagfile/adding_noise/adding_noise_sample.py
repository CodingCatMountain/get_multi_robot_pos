#!/usr/bin/env python3
#coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size

# 定义目标函数
def func(x,a,b,c):
    return a*np.exp(-b*x)+c

# 如果上式要使用math.exp，则需要在return语句中进行列表循环

# 生成x样本点和精确的y样本点
xdata = np.linspace(0,10,100)
# a=3,b=2,c=1
y = func(xdata,3,2,1)

# 加入噪声的方法1:
error1 = 0.1
y_noise1 = error1*np.random.normal(size=xdata.size)
# numpy.random.normal(loc=0.0,scale=1.0,size=None):draw random samples from a normal (Gaussian) distribution
# 生成均值为0,标准差为error1的正态分布(高斯分布)列表,样本点数为size
ydata1 = y+y_noise1

# 加入噪声的方法2:
error2 = 0.2
y_noise2 = error2*np.random.randn(len(xdata))
# numpy.random.randn(d0,d1,...,dn): return a sample (or samples if the n of dn is >=1) from the "standard normal"
# distribution.
# 生成均值为0,标准差为error2的正态分布(高斯分布)列表,样本点数为len(xdata),此处的len(xdata)可以改写为
# xdata.size
ydata2 = y+y_noise2

# 加入噪声的方法3:
error3 = 0.3
ydata3 = [yi*(1.0+(np.random.random()-0.5)*error3) for yi in y]

# numpy.random.random()是[0,1),减去0.5是[-0.5,0.5)，再乘以error3,最后再加上1乘以y,
# 表示产生的数据ydata3夹杂error3%(这里是30%的噪声干扰)

# 注意这里应该使用列表循环，如果直接写成ydata3 = y*(1.0+(np.random.random()-0.5)*error3),那么
# random.random()只会被调用一次，即所有的y中的数据的干扰都是一样的

plt.figure('comparsion between inexact data and exact curve')
plt.plot(xdata,ydata1,'bo',label='inexact data1')
plt.plot(xdata,ydata2,'r+',label='inexact data2')
plt.plot(xdata,ydata3,'y*',label='inexact data3')
plt.plot(xdata,y,'k-',label='exact curve')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()