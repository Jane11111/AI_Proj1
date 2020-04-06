# -*- coding: utf-8 -*-
# @Time    : 2020-03-29 16:53
# @Author  : zxl
# @FileName: test.py

import numpy as np
from datetime import datetime
import math
import matplotlib.pyplot as plt

# def cal(x,y,num):
#     cos_val=sum([x[i]*y[i] for i in range(len(x))])/(np.linalg.norm(x)*np.linalg.norm(y))
#     euc_dist=np.sqrt(sum([(x[k]-y[k])**2 for k in range(len(x))]))
#     print(num+'. 余弦相似度：'+str(cos_val)+', 欧几里得距离：'+str(euc_dist))
#
# x=(1,1,1,1)
# y=(2,2,2,2)
# cal(x,y,'1')
#
# x=(0,1,0,1)
# y=(1,0,1,0)
# cal(x,y,'2')
#
# x=(0,-1,0,1)
# y=(1,0,-1,0)
# cal(x,y,'3')
#
# x=(1,1,0,1,0,1)
# y=(1,1,1,0,0,1)
# cal(x,y,'4')
#
# x=(2,-1,0,2,0,-3)
# y=(-1,1,-1,0,0,-1)
# cal(x,y,'5')



lst=[(0,4),(2,3),(1,9),(7,0)]
for i in range(len(lst)):
    for j in np.arange(i+1,len(lst)):
        arr1=lst[i]
        arr2=lst[j]
        euc_dist=np.sqrt(sum([(arr1[k]-arr2[k])**2 for k in range(len(arr1))]))
        manh_dist=sum([abs(arr1[k]-arr2[k]) for k in range(len(arr1))])
        print('p'+str(i+1)+'与p'+str(j+1)+'的欧式距离：'+str(euc_dist)+ ', 曼哈顿距离：' + str(manh_dist))
