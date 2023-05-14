#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 16:09:58 2023

@author: songyining
"""

from read_data import load_csv
import pandas as pd
import numpy as np



def load_csv(dataPath="23.02.14data filtration.xls"):
    data =pd.read_excel(dataPath) #返回的是DataFrame变量
    cols = data.columns #返回全部列名
    dimensison = data.shape #返回数据的格式，数组，（行数，列数）
    # data.values #返回底层的numpy数据
    row_data = np.array(data.values)#转化为矩阵
    return row_data

#筛选高被引论文
def select():
    data = load_csv()
    #读取论文被引数
    Reference_Count = list(data[:,33])
    pub_year = list(data[:,46])
    paper = data[0:1]
    
    for i in range(1991,2023):
        paper_temp = []
        for j in range(len(pub_year)):
            if pub_year[j] == i:
                paper_temp.append(data[j])
        paper_temp = np.array(paper_temp)#转数据以便排序
        ref_temp = paper_temp[:,33]#找引用量
        rank = np.flipud(np.lexsort((ref_temp,)))#按引用量排序（序号）
        paper_temp = paper_temp[rank]#按序号得到排序结果，以备查找有效文献
        paper = np.r_[paper,paper_temp[0:int(len(paper_temp)/2)]]
    paper = np.delete(paper,0,axis=0)
    return paper

#paper = select()
