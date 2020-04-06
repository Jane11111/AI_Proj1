# -*- coding: utf-8 -*-
# @Time    : 2020-03-31 11:59
# @Author  : zxl
# @FileName: GA.py

import math
import numpy as np
class GA:
    """
    最前面1位表示整数和负数
    接着中间n位表示整数（根据范围而定）
    精确到小数点后2位，用7位来表示小数
    """

    def __init__(self,f,d,NP,min_val,max_val,pm=0.02,pc=0.9):
        """

        :param f: 待优化函数
        :param d: x纬度
        :param min_val:最小值
        :param max_val: 最大值
        :param pm: mutation概率
        :param pc: cross over概率
        """
        integer=max(int(abs(min_val)),int(abs(max_val)))
        self.n1=math.ceil(math.log(integer+1,2))#需要n位表示整数
        self.n2=7#精确到小数点后3位
        self.f=f
        self.d=d
        self.min_val=min_val
        self.max_val=max_val
        self.pm=pm
        self.pc=pc
        self.NP=NP


    def init(self,NP):
        """
        初始化种群
        :param NP:
        :return:
        """
        ndarr=[]
        for i in range(NP):
            arr=np.full(shape=(self.d*(self.n1+self.n2+1),),fill_value=0)
            for j in range(len(arr)):
                epison=np.random.rand()
                if epison>0.5:
                    arr[j]=1
            ndarr.append(arr)
        return np.array(ndarr)

    def decode(self,x):
        """
        将0-1串进行解码，需要解码为一个向量
        :param x:
        :return:
        """
        res=[]
        l=1+self.n1+self.n2
        for i in np.arange(0,len(x),l):
            arr=x[i:i+l]
            v1=0
            v2=0
            for j in np.arange(1,1+self.n1):
                v1+=arr[j]*(2**j)
            for j in np.arange(1+self.n1,len(arr)):
                v2+=arr[j]*(2**(j-1-self.n1))
            while v2>=1:
                v2/=10
            v=v1+v2
            if arr[0]==1:
                v=-v
            if v<self.min_val:
                v=self.min_val
            if v>self.max_val:
                v=self.max_val
            res.append(v)
        return np.array(res)

    def mutation(self,x):
        for i in range(len(x)):
            epison=np.random.rand()
            if epison>self.pm:
                x[i]=1-x[i]
        return x

    def crossover(self,p1,p2):
        """
        单切点交叉
        :param p1: 父亲
        :param p2: 母亲
        :return:
        """
        epison=np.random.rand()
        if epison>self.pc:
            return p1,p2
        idx1=np.random.randint(low=0,high=len(p1))
        idx2=idx1
        while idx2==idx1:
            idx2=np.random.randint(low=0,high=len(p1))
        res1=[]
        res2=[]
        tmp=idx1
        idx1=min(idx1,idx2)
        idx2=max(tmp,idx2)

        res1.extend(p1[:idx1])
        res1.extend(p2[idx1:idx2])
        res1.extend(p1[idx2:])

        res2.extend(p2[:idx1])
        res2.extend(p1[idx1:idx2])
        res2.extend(p2[idx2:])

        return [np.array(res1),np.array(res2)]



    def select(self,p_lst):
        """
        选择父亲
        :param p_lst:每一个父亲对应概率
        :return:选择的idx
        """
        epison=np.random.rand()
        v=0
        for i in range(len(p_lst)):
            if v<=epison<v+p_lst[i]:
                return i
            v+=p_lst[i]
        return len(p_lst)-1


    def cal_fitness(self,x):
        """
        计算当前fitness值
        :param x:0-1表示的串
        :return:
        """
        # origin_x=x.copy()
        x1=self.decode(x.copy())
        # print(x==origin_x)
        # x2=self.decode(x.copy())
        return -self.f(x1)

    def opt(self,NG):
        ndarr=self.init(self.NP)
        min_lst=[]
        max_lst=[]
        mean_f=[]
        fitness_lst=[]
        a=self.cal_fitness(ndarr[0])
        b=self.cal_fitness(ndarr[0])
        for i in range(len(ndarr)):
            fitness_lst.append(self.cal_fitness(ndarr[i]))

        for i in range(NG):

            min_lst.append(-np.max(fitness_lst))
            max_lst.append(-np.min(fitness_lst))
            mean_f.append(np.mean(fitness_lst))
            p_lst=[]
            m1=min(fitness_lst)
            m2=max(fitness_lst)
            for item in fitness_lst:
                p_lst.append((item-m1)/(m2-m1))

            new_ndarr=[]
            new_fitness_lst=[]
            #变异，交叉，选择操作
            for j in range(int(self.NP)):
                #论盘法选父亲
                # print("operation:%d"%j)
                p1_idx=self.select(p_lst)
                p2_idx=self.select(p_lst)
                #变异
                p1 = ndarr[p1_idx].copy()
                p2 = ndarr[p2_idx].copy()
                new_ndarr.append(self.mutation(p1.copy()))
                new_ndarr.append(self.mutation(p1.copy()))
                new_fitness_lst.append(self.cal_fitness(new_ndarr[-2]))
                new_fitness_lst.append(self.cal_fitness(new_ndarr[-1]))
                #交叉
                child1,child2=self.crossover(p1,p2)
                new_fitness_lst.append(self.cal_fitness(child1))
                new_fitness_lst.append(self.cal_fitness(child2))
                new_ndarr.append(child1)
                new_ndarr.append(child2)

            ndarr=list(ndarr)
            ndarr.extend(new_ndarr)
            fitness_lst.extend(new_fitness_lst)

            #更新种群，选fitness大的
            sort_idx=np.argsort(fitness_lst)
            ndarr=np.array(ndarr)
            ndarr=ndarr[sort_idx[-self.NP:]]
            fitness_lst=list(np.array(fitness_lst)[sort_idx[-self.NP:]])

        best_idx=np.argsort(fitness_lst)[-1]
        best_arr=self.decode(ndarr[best_idx])
        best_fitness=fitness_lst[best_idx]
        return (min_lst,max_lst,best_arr,-best_fitness)

