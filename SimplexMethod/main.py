# -*- coding: utf-8 -*-
# @Time    : 2020-03-31 23:03
# @Author  : zxl
# @FileName: main.py

import math
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
from SimplexMethod.Simplex import Simplex
from SimplexMethod.GA import GA
from SimplexMethod.DE import DE


def f1(x):
    res=0
    for i in range(len(x)):
        res+=(i+1)*x[i]*x[i]
    return res

def f2(x):
    res=0
    for i in range(len(x)-1):
        res+=100*(x[i+1]-x[i]**2)**2+(1-x[i])**2
    return res

def f3(x):
    r1=0
    r2=0
    d=len(x)
    for i in range(d):
        r1+=x[i]**2
        r2+=math.cos(2*math.pi*x[i])
    res=-20*math.pow(math.e,-0.2*math.sqrt(r1/d))-math.pow(math.e,r2/d)+20+math.pow(math.e,1)
    return res

def f4(x):
    r1=0
    r2=1
    for i in range(len(x)):
        r1+=x[i]**2/4000
        r2*=math.cos(x[i]/math.sqrt(i+1))
    return 1+r1-r2


def draw1(f,min_val,max_val,max_iter,d,N,title):
    """
    迭代次数，每轮迭代最小值
    """
    ds_opt_method1 = Simplex(f, d, min_val, max_val)
    ga_opt_method1 = GA(f, d, N, min_val, max_val)
    de_opt_method1 = DE(f, d, N, min_val, max_val)
    (ds_min_y_lst1, dsmax_y_lst1, ds_best_x1, ds_best_y1) = ds_opt_method1.opt(max_iter)
    (ga_min_y_lst1, ga_max_y_lst1, ga_best_x1, ga_best_y1) = ga_opt_method1.opt(max_iter)
    (de_min_y_lst1, de_max_y_lst1, de_best_x1, de_best_y1) = de_opt_method1.opt(max_iter)
    print(ds_best_x1)
    print(ds_best_y1)
    print(ga_best_x1)
    print(ga_best_y1)
    print(de_best_x1)
    print(de_best_y1)
    plt.plot(range(max_iter), ds_min_y_lst1, c='green')
    plt.plot(range(max_iter), ga_min_y_lst1, c='b')
    plt.plot(range(max_iter), de_min_y_lst1, c='r')
    plt.title(title)
    plt.legend(['simplex', 'GA', 'DE'])
    plt.xlabel('iteration')
    plt.ylabel('best_y')
    plt.show()
    plt.plot(range(max_iter), ds_min_y_lst1, c='green')
    plt.plot(range(max_iter), de_min_y_lst1, c='r')
    plt.title(title)
    plt.legend(['simplex', 'DE'])
    plt.xlabel('iteration')
    plt.ylabel('best_y')
    plt.show()

def draw2(f,min_val,max_val,max_iter,d,N,title):
    """
    d,运行时间
    """
    lst=[]
    for d in [5,10,30,50]:
        ds_opt_method1 = Simplex(f, d, min_val, max_val)
        ga_opt_method1=GA(f,d,N,min_val,max_val)
        de_opt_method1=DE(f,d,N,min_val,max_val)
        t1=time.clock()
        res=ds_opt_method1.opt(max_iter)
        t2=time.clock()
        res=ga_opt_method1.opt(max_iter)
        t3=time.clock()
        res=de_opt_method1.opt(max_iter)
        t4=time.clock()
        lst.append([t2 - t1, t3 - t2, t4 - t3])

    lst=np.array(lst)
    ind = np.arange(len(lst[:,0]))  # the x locations for the groups
    width = 0.35  # the width of the bars
    for item in lst:
        print(item)

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width, lst[:,0], width, color='green', label='simplex',alpha=0.6)
    for x, y in zip(ind-width, lst[:,0]):
        plt.text(x + 0.05, y + 0.05, '%.3f' % y, ha='center', va='bottom')
    rects2 = ax.bar(ind , lst[:,1], width, color='b', label='GA',alpha=0.6)
    for x, y in zip(ind , lst[:, 1]):
        plt.text(x + 0.05, y + 0.05, '%.3f' % y, ha='center', va='bottom')
    rects2 = ax.bar(ind + width , lst[:,2], width, color='r', label='DE',alpha=0.6)
    for x, y in zip(ind + width, lst[:, 2]):
        plt.text(x + 0.05, y + 0.05, '%.3f' % y, ha='center', va='bottom')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('dimension')
    ax.set_ylabel('running time/s')
    ax.set_title(title)
    plt.xticks(ind, ('5','10','30','50'))
    ax.legend()

    plt.show()

def draw3(f,min_val,max_val,max_iter,d,N_lst,title):
    min_y_lst=[]
    color_lst=['b','g','orange','r','y']
    for N in N_lst:
        opt_method = DE(f, d, N, min_val, max_val)
        (de_min_y_lst1, de_max_y_lst1, de_best_x1, de_best_y1) = opt_method.opt(max_iter)
        min_y_lst.append(de_min_y_lst1)
    fig, ax = plt.subplots()
    for i in range(len(N_lst)):
        ax.plot(range(max_iter),min_y_lst[i],color=color_lst[i],label='N='+str(N_lst[i]))
    ax.legend(['N = '+str(i) for i in N_lst])
    ax.set_title('DE Method  '+title)
    ax.set_xlabel('iteration')
    ax.set_ylabel('best_y')
    plt.show()
def draw4(f,min_val,max_val,max_iter,d,N_lst,title):
    min_y_lst=[]
    color_lst=['b','g','orange','r','y']
    for N in N_lst:
        opt_method = GA(f, d, N, min_val, max_val)
        (de_min_y_lst1, de_max_y_lst1, de_best_x1, de_best_y1) = opt_method.opt(max_iter)
        min_y_lst.append(de_min_y_lst1)
    fig, ax = plt.subplots()
    for i in range(len(N_lst)):
        ax.plot(range(max_iter),min_y_lst[i],color=color_lst[i],label='N='+str(N_lst[i]))
    ax.legend(['N = '+str(i) for i in N_lst])
    ax.set_title('GA Method  '+title)
    ax.set_xlabel('iteration')
    ax.set_ylabel('best_y')
    plt.show()
def draw5(f,min_val,max_val,max_iter,d,N,title):
    min_y_lst = []
    color_lst = ['b', 'g', 'orange', 'r', 'y']
    label_lst=['rand/1','best/1','current to best/1','best/2','rand/2']
    opt_method = DE(f, d, N, min_val, max_val)
    (de_min_y_lst1, de_max_y_lst1, de_best_x1, de_best_y1) = opt_method.opt(max_iter)
    min_y_lst.append(de_min_y_lst1)
    (de_min_y_lst2, de_max_y_lst2, de_best_x2, de_best_y2) = opt_method.opt2(max_iter)
    min_y_lst.append(de_min_y_lst2)
    (de_min_y_lst3, de_max_y_lst3, de_best_x3, de_best_y3) = opt_method.opt3(max_iter)
    min_y_lst.append(de_min_y_lst3)
    (de_min_y_lst4, de_max_y_lst4, de_best_x4, de_best_y4) = opt_method.opt4(max_iter)
    min_y_lst.append(de_min_y_lst4)
    (de_min_y_lst5, de_max_y_lst5, de_best_x5, de_best_y5) = opt_method.opt5(max_iter)
    min_y_lst.append(de_min_y_lst5)

    fig, ax = plt.subplots()
    for i in range(len(min_y_lst)):
        ax.plot(range(max_iter), min_y_lst[i], color=color_lst[i])
    ax.legend(label_lst)
    ax.set_title('DE Method  ' + title)
    ax.set_xlabel('iteration')
    ax.set_ylabel('best_y')
    plt.show()


if __name__ == "__main__":

    d=5
    N=50
    max_iter=50
    N_lst=[20,50,100,500]

    min_val = -5.12
    max_val = 5.12
    # draw1(f1,min_val,max_val,max_iter,d,N,'F1: Ellipsoid Problem')
    # draw2(f1,min_val,max_val,max_iter,d,N,'F1: Ellipsoid Problem')
    # draw3(f1, min_val, max_val, max_iter, d, N_lst, 'F1: Ellipsoid Problem')
    # draw4(f1, min_val, max_val, max_iter, d, N_lst, 'F1: Ellipsoid Problem')
    draw5(f1, min_val, max_val, max_iter, d, N, 'F1: Ellipsoid Problem')

    min_val = -2.048
    max_val = 2.048
    max_iter=100
    # draw1(f2,min_val,max_val,max_iter,d,N,'F2: Rosenbrock Problem')
    # draw2(f2, min_val, max_val, max_iter, d, N, 'F2: Rosenbrock Problem')
    # draw3(f2, min_val, max_val, max_iter, d, N_lst, 'F2: Rosenbrock Problem')
    # draw4(f2, min_val, max_val, max_iter, d, N_lst, 'F2: Rosenbrock Problem')
    draw5(f2, min_val, max_val, max_iter, d, N, 'F2: Rosenbrock Problem')

    max_iter=50
    min_val = -32.768
    max_val = 32.768
    # draw1(f3,min_val,max_val,max_iter,d,N,'F3: Ackley Problem')
    # draw2(f3, min_val, max_val, max_iter, d, N, 'F3: Ackley Problem')
    # draw3(f3, min_val, max_val, max_iter, d, N_lst, 'F3: Ackley Problem')
    # draw4(f3, min_val, max_val, max_iter, d, N_lst, 'F3: Ackley Problem')
    draw5(f3, min_val, max_val, max_iter, d, N, 'F3: Ackley Problem')

    min_val = -600
    max_val = 600
    # draw1(f4,min_val,max_val,max_iter,d,N,'F4: Griewank Problem')
    # draw2(f4,min_val,max_val,max_iter,d,N,'F4: Griewank Problem')
    # draw3(f4,min_val,max_val,max_iter,d,N_lst,'F4: Griewank Problem')
    # draw4(f4,min_val,max_val,max_iter,d,N_lst,'F4: Griewank Problem')
    draw5(f4, min_val, max_val, max_iter, d, N, 'F4: Griewank Problem')






