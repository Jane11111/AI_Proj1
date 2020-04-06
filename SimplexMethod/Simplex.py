# -*- coding: utf-8 -*-
# @Time    : 2020-03-29 16:38
# @Author  : zxl
# @FileName: Simplex.py

import math
import numpy as np

#TODO 什么时候restart
class Simplex():

    def __init__(self,f,d,min_val,max_val):
        """
        :param f:待优化问题
        :param d:变量纬度
        """
        self.f=f
        self.d=d
        self.min_val=min_val
        self.max_val=max_val

    def reflection(self,x,x_ndarr):
        """
        将x按照x_ndarr形成的平面进行反射
        :param x:
        :param x_ndarr:
        :return:
        """
        center_x=np.mean(x_ndarr,axis=0)
        return self.norm_x(center_x*2-x)

    def expansion(self,origin_x,target_x):
        """
        将target_x 沿着origin_x -> target_x 方向扩张
        :param origin_x:
        :param target_x:
        :return:
        """
        return self.norm_x(0.5*(target_x-origin_x)+target_x)

    def contraction(self,x,x_ndarr):
        """
        将x沿着其于x_ndarr中心方向收缩
        :param x:
        :param x_ndarr:
        :return:
        """
        x_center=np.mean(x_ndarr,axis=0)
        return self.norm_x((x+x_center)/2)

    def shrink(self,x_ndarr,x_best):
        """
        将x_ndarr朝着x方向shrink
        :param x_ndarr:
        :param x_best:
        :return:
        """
        new_x_ndarr=[]
        for arr in x_ndarr:
            new_arr=np.mean(np.array([arr,x_best]),axis=0)
            new_x_ndarr.append(new_arr)
        return self.norm_x(np.array(new_x_ndarr))

    def init(self,arr=None):
        """
        保证arr在ndarr里面
        :param arr:
        :return:
        """
        ndarr=[]
        if arr is not None:
            ndarr.append(arr)
        while len(ndarr)< self.d+1:
            ndarr.append(np.random.rand(self.d,))

        ndarr = np.array(ndarr)
        return self.norm_x(ndarr)

    def cal_y(self,x_ndarr):
        y_arr=[]
        for arr in x_ndarr:
            y=self.f(arr)
            y_arr.append(y)
        return np.array(y_arr)

    def norm_x(self,x_arr):
        if len(x_arr.shape)==1:
            for i in range(x_arr.shape[0]):
                if x_arr[i]<self.min_val:
                    x_arr[i]=self.min_val
                elif x_arr[i]>self.max_val:
                    x_arr[i]=self.max_val
        else:
            for i in range(x_arr.shape[0]):
                for j in range(x_arr.shape[1]):
                    if x_arr[i][j]<self.min_val:
                        x_arr[i][j]=self.min_val
                    elif x_arr[i][j]>self.max_val:
                        x_arr[i][j]=self.max_val
        return x_arr


    def opt(self,max_ietr=500):
        """
        开始进行优化
        TODO 何时停止迭代
        TODO 何时restart
        :return: 迭代次数，最优解
        """
        x_ndarr=self.init()
        y_arr=self.cal_y(x_ndarr)
        idx_y=np.argsort(y_arr)#对应y_arr中从小到大索引
        min_y_lst=[]#记录每一次迭代时候，最小的y
        max_y_lst=[]#记录每一次迭代时候，最大的y
        for i in range(max_ietr):
            refl_x=self.reflection(x_ndarr[idx_y[-1]],x_ndarr[idx_y[:-1]])
            refl_y=self.f(refl_x)
            if refl_y<y_arr[idx_y[0]]:#reflection resulted in best value so far
                expa_x=self.expansion(x_ndarr[idx_y[-1]],refl_x)
                expa_y=self.f(expa_x)
                x_ndarr[idx_y[-1]]=expa_x
                y_arr[idx_y[-1]]=expa_y
            elif refl_y<y_arr[idx_y[-2]]: # reflection helps , keep it
                x_ndarr[idx_y[-1]] = refl_x
                y_arr[idx_y[-1]] = refl_y
            else: #reflection does not help
                cont_x=self.contraction(x_ndarr[idx_y[-1]],x_ndarr[idx_y[:-1]])
                cont_y=self.f(cont_x)
                if cont_y<y_arr[idx_y[-2]]:#contraction helps
                    x_ndarr[idx_y[-1]]=cont_x
                    y_arr[idx_y[-1]]=cont_y
                else:
                    new_arr=self.shrink(x_ndarr[idx_y[:-1]],x_ndarr[idx_y[0]])
                    x_ndarr=np.concatenate((new_arr,[x_ndarr[idx_y[0]]]))
                    y_arr=self.cal_y(x_ndarr)

            idx_y=np.argsort(y_arr)
            min_y_lst.append(y_arr[idx_y[0]])
            max_y_lst.append(y_arr[idx_y[-1]])


        return (min_y_lst,max_y_lst,x_ndarr[idx_y[0]],y_arr[idx_y[0]])












