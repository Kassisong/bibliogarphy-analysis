#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 19:15:49 2023

@author: songyining
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_csv(dataPath = "23.02.14data filtration.xls"):
    data =pd.read_excel(dataPath) #返回的是DataFrame变量
    cols = data.columns #返回全部列名
    dimensison = data.shape #返回数据的格式，数组，（行数，列数）
    # data.values #返回底层的numpy数据
    row_data = np.array(data.values)#转化为矩阵
    return row_data

#绘制论文发表年份图[折线图]
def publish_count(pub_year):
    x = []
    pub_num = []
    for i in range(1967,2023):
        x.append(i)
        pub_num.append(pub_year.count(i))
    
    #绘图以及调格式
    plt.figure(figsize=(16,6))
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"
    plt.scatter(x,pub_num,color='skyblue')
    plt.plot(x,pub_num,'.-')
    xz = range(1967,2023)
    yz = range(0,60,5)
    plt.xticks(xz)
    plt.yticks(yz)
    plt.grid(axis="y")
    w,e=plt.xticks()
    plt.setp(e,rotation=60)
    plt.xlabel('Year')
    plt.ylabel('Public Number')
    
    plt.savefig('1-1.eps', format='eps',bbox_inches='tight')
    return()


if __name__ == '__main__':
    data = load_csv()
    pub_year = list(data[:,46])
    publish_count(pub_year)