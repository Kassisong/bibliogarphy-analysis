#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 21:51:46 2023

@author: songyining
"""

import numpy as np
np.set_printoptions(suppress=True)#不已科学记数法输出
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import networkx as nx

def load_csv():
    dataPath = "23.02.14data filtration.xls"
    data =pd.read_excel(dataPath) #返回的是DataFrame变量
    cols = data.columns #返回全部列名
    dimensison = data.shape #返回数据的格式，数组，（行数，列数）
    # data.values #返回底层的numpy数据
    row_data = np.array(data.values)#转化为矩阵
    return row_data
data = load_csv()
#读取论文发表年份信息
year = data[:,46]

author = data[:,1]
author_set = []
for i in range(len(author)):
    a = ''.join(str(i) for i in author[i])
    a = a.upper()
    a = a.replace(" ", "")
    a = a.replace('\'', '')
    a = a.replace('-', '')
    a = a.replace('.', '')
    if 'LYNCH' in a and 'LYNCH,RS' not in a:
        a = a.replace('LYNCH,R', 'LYNCH,RS')
    if 'KEITH' in a and 'KEITH,MJ' not in a:
        a = a.replace('KEITH,M', 'KEITH,MJ')
    if 'STAPPERS' in a and 'STAPPERS,BW' not in a:
        a = a.replace('STAPPERS,B', 'STAPPERS,BW')
    if 'BIWER,C' in a and 'BIWER,CM' not in a:
        a = a.replace('BIWER,C', 'BIWER,CM')
    if 'CEPEDA,C' in a and 'CEPEDA,CB' not in a:
        a = a.replace('CEPEDA,C', 'CEPEDA,CB')
    if 'CHENG,H' in a and 'CHENG,HP' not in a:
        a = a.replace('CHENG,H', 'CHENG,HP')
    if 'COHEN,D' in a and 'COHEN,DE' not in a:
        a = a.replace('COHEN,D', 'COHEN,DE')
    if 'COOPER,S' in a and 'COOPER,SJ' not in a:
        a = a.replace('COOPER,S', 'COOPER,SJ')
    if 'CORNISH,N' in a and 'CORNISH,NJ' not in a:
        a = a.replace('CORNISH,N', 'CORNISH,NJ')
    if 'DEROSA,R' in a and 'DEROSA,RT' not in a:
        a = a.replace('DEROSA,R', 'DEROSA,RT')
    if 'DIAZ,M' in a and 'DIAZ,MC' not in a:
        a = a.replace('DIAZ,M', 'DIAZ,MC')
    if 'ELLIS,J' in a and 'ELLIS,JA' not in a:
        a = a.replace('ELLIS,J', 'ELLIS,JA')
    if 'HOBBS,G' in a and 'HOBBS,GB' not in a:
        a = a.replace('HOBBS,G', 'HOBBS,GB')
    if 'JENET,F' in a and 'JENET,FA' not in a:
        a = a.replace('JENET,F', 'JENET,FA')
    if 'LYNE,A' in a and 'LYNE,AG' not in a:
        a = a.replace('LYNE,A', 'LYNE,AG')
    if 'MCLAUGHLIN,M' in a and 'MCLAUGHLIN,MA' not in a:
        a = a.replace('MCLAUGHLIN,M', 'MCLAUGHLIN,MA')
    if 'SARKISSIAN,J' in a and 'SARKISSIAN,JM' not in a:
        a = a.replace('SARKISSIAN,J', 'SARKISSIAN,JM')
    if 'SHANNON,R' in a and 'SHANNON,RM' not in a:
        a = a.replace('SHANNON,R', 'SHANNON,RM')
    if 'SWIGGUM,J' in a and 'SWIGGUM,JK' not in a:
        a = a.replace('SWIGGUM,J', 'SWIGGUM,JK')
    
    a = a.split(';',500)
    author_set.append(a)


######绘图
start = min(year)
end = max(year)+1

interval = 5

author_num = np.zeros([3,int((end-start)/interval)])
for i in range(1,12,interval):
    author_year_temp = []
    for j in range(len(author_set)):
        if i <10:
            if i <= len(author_set[j]) and i+interval > len(author_set[j]):
                author_year_temp.append(year[j]) 
        else:
            if i <= len(author_set[j]):
                author_year_temp.append(year[j])
 
    for j in range(start,end,interval):
        num = 0
        for k in author_year_temp:
            if j <= k and j+interval > k:
                num +=1
        author_num[int((i-1)/interval),int((j-start)/interval)] = num

author_num = author_num/sum(author_num)

plt.figure(figsize=(12, 6), dpi=100)
x = range(int(start+interval/2),int(end+interval/2),interval)

plt.plot(x,author_num[0],marker='o',label='1-5')
plt.plot(x,author_num[1],marker='o',label='6-10')
plt.plot(x,author_num[2],marker='o',label='>'+str(10))

xz = range(start,end+3,interval)
yz = np.arange(0,1,0.1)
plt.xticks(xz)
plt.yticks(yz)

from matplotlib.ticker import FuncFormatter
def to_percent(temp, position):
    return '%1.0f'%(100*temp) + '%'

plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))


plt.legend()
plt.xlabel('Year')
plt.ylabel('Number of co-authors (%)')

