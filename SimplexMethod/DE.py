# -*- coding: utf-8 -*-
# @Time    : 2020-04-01 09:25
# @Author  : zxl
# @FileName: DE.py

import numpy as np

class DE:
    def __init__(self,f,d,N,min_val,max_val,cr=0.3,F=0.5):
        """

        :param f: 待优化方法
        :param d: x纬度
        :param N: 种群数目
        :param min_val: x范围最小值
        :param max_val: x范围最大值
        :param cr: combination步骤的cr，是否combine
        :param F: 步长
        """
        self.f=f
        self.d=d
        self.N=N
        self.min_val=min_val
        self.max_val=max_val
        self.cr=cr
        self.F=F

    def init(self):
        ndarr=np.random.rand(self.N,self.d)
        return self.norm_x(ndarr)

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

    def mutation(self,x1,x2,x3):
        return self.norm_x(x1+self.F*(x2-x3))
    def mutation2(self,x1,x2,best):
        return self.norm_x(best+self.F*(x1-x2))
    def mutation3(self,x1,x2,xi,best):
        return self.norm_x(xi+self.F*(best-xi)+self.F*(x1-x2))
    def mutation4(self,x1,x2,x3,x4,best):
        return self.norm_x(best+self.F*(x1-x2)+self.F*(x3-x4))
    def mutation5(self,x1,x2,x3,x4,x5):
        return self.norm_x(x1+self.F*(x2-x3)+self.F*(x4-x5))


    def recombination(self,x,v,I):
        for i in range(len(v)):
            if i==I:
                v[i]=x[i]
                continue
            epison=np.random.rand()
            if epison>self.cr:
                v[i]=x[i]
        return self.norm_x(v)

    def selection(self,x,u):
        if self.f(u)<=self.f(x):
            return u
        return x
    


    def opt(self,max_iter):

        ndarr=self.init()
        min_lst=[]
        max_lst=[]

        for k in range(max_iter):
            y_lst=[]
            for arr in ndarr:
                y_lst.append(self.f(arr))
            min_lst.append(np.min(y_lst))
            max_lst.append(np.max(y_lst))
            new_ndarr=ndarr
            for i in range(self.N):
                r1=i
                r2=i
                r3=i
                while r1==i:
                    r1=np.random.randint(0,self.N)
                while r2==i or r2==r1:
                    r2=np.random.randint(0,self.N)
                while r3==i or r3==r2 or r3==r1:
                    r3=np.random.randint(0,self.N)
                v=self.mutation(ndarr[r1],ndarr[r2],ndarr[r3])
                I=np.random.randint(0,self.d)
                u=self.recombination(ndarr[i],v,I)
                new_ndarr[i]=self.selection(ndarr[i],u)
            ndarr=new_ndarr
        y_lst=[]
        for arr in ndarr:
            y_lst.append(self.f(arr))
        idx=np.argsort(y_lst)[0]
        best_x=ndarr[idx]
        best_y=y_lst[idx]
        return (min_lst,max_lst,best_x,best_y)


    def opt2(self,max_iter):
        ndarr = self.init()
        min_lst = []
        max_lst = []

        for k in range(max_iter):
            y_lst = []
            for arr in ndarr:
                y_lst.append(self.f(arr))
            min_lst.append(np.min(y_lst))
            max_lst.append(np.max(y_lst))
            x_best=ndarr[np.argsort(y_lst)[0]]
            new_ndarr = ndarr
            for i in range(self.N):
                r1 = i
                r2 = i
                r3 = i
                while r1 == i:
                    r1 = np.random.randint(0, self.N)
                while r2 == i or r2 == r1:
                    r2 = np.random.randint(0, self.N)

                v = self.mutation2(ndarr[r1], ndarr[r2], x_best)

                I = np.random.randint(0, self.d)
                u = self.recombination(ndarr[i], v, I)
                new_ndarr[i] = self.selection(ndarr[i], u)
            ndarr = new_ndarr
        y_lst = []
        for arr in ndarr:
            y_lst.append(self.f(arr))
        idx = np.argsort(y_lst)[0]
        best_x = ndarr[idx]
        best_y = y_lst[idx]
        return (min_lst, max_lst, best_x, best_y)

    def opt3(self,max_iter):
        ndarr = self.init()
        min_lst = []
        max_lst = []

        for k in range(max_iter):
            y_lst = []
            for arr in ndarr:
                y_lst.append(self.f(arr))
            min_lst.append(np.min(y_lst))
            max_lst.append(np.max(y_lst))
            x_best = ndarr[np.argsort(y_lst)[0]]
            new_ndarr = ndarr
            for i in range(self.N):
                r1 = i
                r2 = i
                r3 = i
                while r1 == i:
                    r1 = np.random.randint(0, self.N)
                while r2 == i or r2 == r1:
                    r2 = np.random.randint(0, self.N)
                v = self.mutation3(ndarr[r1], ndarr[r2], ndarr[i],x_best)
                I = np.random.randint(0, self.d)
                u = self.recombination(ndarr[i], v, I)
                new_ndarr[i] = self.selection(ndarr[i], u)
            ndarr = new_ndarr
        y_lst = []
        for arr in ndarr:
            y_lst.append(self.f(arr))
        idx = np.argsort(y_lst)[0]
        best_x = ndarr[idx]
        best_y = y_lst[idx]
        return (min_lst, max_lst, best_x, best_y)


    def opt4(self,max_iter):
        ndarr = self.init()
        min_lst = []
        max_lst = []

        for k in range(max_iter):
            y_lst = []
            for arr in ndarr:
                y_lst.append(self.f(arr))
            min_lst.append(np.min(y_lst))
            max_lst.append(np.max(y_lst))
            x_best = ndarr[np.argsort(y_lst)[0]]
            new_ndarr = ndarr
            for i in range(self.N):
                r1 = i
                r2 = i
                r3 = i
                r4 = i
                while r1 == i:
                    r1 = np.random.randint(0, self.N)
                while r2 == i or r2 == r1:
                    r2 = np.random.randint(0, self.N)
                while r3 == i or r3 == r2 or r3 == r1:
                    r3 = np.random.randint(0, self.N)
                while r4 == i or r4 == r3 or r4 == r2 or r4 == r1:
                    r4 = np.random.randint(0, self.N)
                v = self.mutation4(ndarr[r1], ndarr[r2], ndarr[r3],ndarr[r4],x_best)
                I = np.random.randint(0, self.d)
                u = self.recombination(ndarr[i], v, I)
                new_ndarr[i] = self.selection(ndarr[i], u)
            ndarr = new_ndarr
        y_lst = []
        for arr in ndarr:
            y_lst.append(self.f(arr))
        idx = np.argsort(y_lst)[0]
        best_x = ndarr[idx]
        best_y = y_lst[idx]
        return (min_lst, max_lst, best_x, best_y)

    def opt5(self,max_iter):
        ndarr = self.init()
        min_lst = []
        max_lst = []

        for k in range(max_iter):
            y_lst = []
            for arr in ndarr:
                y_lst.append(self.f(arr))
            min_lst.append(np.min(y_lst))
            max_lst.append(np.max(y_lst))
            new_ndarr = ndarr
            for i in range(self.N):
                r1 = i
                r2 = i
                r3 = i
                r4 = i
                r5 = i
                while r1 == i:
                    r1 = np.random.randint(0, self.N)
                while r2 == i or r2 == r1:
                    r2 = np.random.randint(0, self.N)
                while r3 == i or r3 == r2 or r3 == r1:
                    r3 = np.random.randint(0, self.N)
                while r4 == i or r4 == r3 or r4 == r2 or r4 == r1:
                    r4 = np.random.randint(0, self.N)
                while r5 == i or r5 == r4 or r5 == r3 or r5 == r2 or r5 == r1:
                    r5=np.random.randint(0,self.N)
                v = self.mutation5(ndarr[r1], ndarr[r2], ndarr[r3], ndarr[r4], ndarr[r5])
                I = np.random.randint(0, self.d)
                u = self.recombination(ndarr[i], v, I)
                new_ndarr[i] = self.selection(ndarr[i], u)
            ndarr = new_ndarr
        y_lst = []
        for arr in ndarr:
            y_lst.append(self.f(arr))
        idx = np.argsort(y_lst)[0]
        best_x = ndarr[idx]
        best_y = y_lst[idx]
        return (min_lst, max_lst, best_x, best_y)
