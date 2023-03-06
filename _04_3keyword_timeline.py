#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 20:37:33 2023

@author: songyining
"""

import matplotlib.pyplot as plt
import wordcloud as wc
from read_data import Read_Data
from read_data import load_csv
import pandas as pd
import numpy as np
import networkx as nx
from _00_2core_paper import select



def load_csv(dataPath="23.02.14data filtration.xls"):
    data =pd.read_excel(dataPath) #返回的是DataFrame变量
    cols = data.columns #返回全部列名
    dimensison = data.shape #返回数据的格式，数组，（行数，列数）
    # data.values #返回底层的numpy数据
    row_data = np.array(data.values)#转化为矩阵
    return row_data

def words():
    data = load_csv()
    #按年份排序，便于排序
    idex=np.lexsort([data[:,46]])
    sorted_data = data[idex, :]
    
    print(len(data))
    
    pub_year = list(sorted_data[:,46])
    
    keywords = list(sorted_data[:,19])
    keywords_set = []
    for i in range(len(keywords)):
        if type(keywords[i]) == float:
            keywords_set.append(list('0'))
        else:
            a = ''.join(str(i) for i in keywords[i])
            a = a.lower()                                    #全部小写，统一格式
            #a = ''.join([i for i in a if not i.isdigit()])   #删除数字
            a = a.split(';',300)                        #关键词划分
            b = []
            for j in range(len(a)):
                a1 = a[j]
                a1 = a1.strip()
                if ' : ' in a1:   
                    a1 = a1.replace(' : ',': ')
                if ', ' in a1:   
                    a1 = a1.replace(', ',': ')
                if '(' in a1:   
                    a1 = a1.replace('(','')
                if ')' in a1:   
                    a1 = a1.replace(')','') 
                  
            
                if 'pulsars: general' in a1:
                    a1 = 'pulsars: general'
                if 'pulsars: individual' in a1:
                    a1 = 'pulsars: general'
                if 'pulsars' in a1 and 'pulsars: general' not in a1:   
                    a1 = a1.replace('pulsars','pulsars: general')
                if 'pulsar' in a1 and 'pulsars: general' not in a1:   
                    a1 = a1.replace('pulsar', 'pulsars: general')
                if 'searching' in a1:   
                    a1 = a1.replace('searching', 'search')
                if 'timing arrays' in a1:   
                    a1 = a1.replace('timing arrays', 'timing array')
                if 'magnetic fields' in a1:   
                    a1 = a1.replace('magnetic fields', 'magnetic field')
                if 'astronomy data analysis' in a1:   
                    a1 = a1.replace('astronomy data analysis', 'data analysis')
                # if 'neutron' in a1 and 'neutron stars' not in a1:   
                #     a1 = a1.replace('neutron', 'neutron star')
                if 'neutron stars' in a1:   
                    a1 = a1.replace('neutron stars', 'neutron star')
                    
                if 'methods: data analysis' in a1:   
                    a1 = a1.replace('methods: data analysis', 'data analysis')   
                if 'neutron stars star' in a1:   
                    a1 = a1.replace('neutron stars star', 'neutron star')   
                if 'general:general' in a1:   
                    a1 = a1.replace('general:general', 'general')
                if 'stars: pulsars: general general' in a1:   
                    a1 = a1.replace('stars: pulsars: general general', 'general')
                if 'fields' in a1:   
                    a1 = a1.replace('fields', 'field')
                    
                if 'discs' in a1:
                    a1 = a1.replace('discs','disks')
                    
                if 'globular clusters: individual' in a1:
                    a1 = 'globular clusters: individual'
                if 'stars: individual' in a1:
                    a1 = 'stars: individual'
                if 'supernovae: individual' in a1:
                    a1 = 'supernovae: general'
                if 'x-rays: individual' in a1:
                    a1 = 'x-rays: general'
                if 'x-rays stars' in a1:
                    a1 = 'x-rays: general'
                if 'x-rays: stars' in a1:
                    a1 = 'x-rays: general'
                if 'gamma rays' in a1:
                    a1 = a1.replace('gamma rays','gamma-rays')
                    
                if 'radio continuum' in a1 and 'radio continuum: general' not in a1:
                    a1 = a1.replace('radio continuum','radio continuum: general')
                if 'radio continuum: stars' in a1:
                    a1 = a1.replace('radio continuum: stars','radio continuum: general')     
                if 'stars: neutron' in a1:
                    a1 = a1.replace('stars: neutron','neutron stars')
                if 'radio continuum: general: stars' in a1:
                    a1 = a1.replace('radio continuum: general: stars','radio continuum: general')    
                if 'binaries close' in a1:
                    a1 = a1.replace('binaries close','binaries: close')
                if 'gravitational wave astronomy' in a1:
                    a1 = 'gravitational waves'
                
                
                if 'survey' in a1 and 'surveys' not in a1:
                    a1 = a1.replace('survey','surveys')
                if 'catalogs' in a1:
                    a1 = a1.replace('catalogs','catalogues')
        
              
                b.append(a1)                                      #删除关键词前空格
            keywords_set.append(b)
    return keywords_set, pub_year 


def frequency(para,top_N):
    temp = sum(para,[])
    j = 0 
    for i in range(len(temp)):
        if temp[j] == '0':
            temp.pop(j)
        else:
            j += 1
    para_num = pd.DataFrame(temp)[0].value_counts()[:top_N]
    return para_num


keywords, pub_year  = words()
key = frequency(keywords,61)


###找到要画的数据
keywords_list = []
keywords_year = []
node_size = []
for i in range(len(keywords)):
    for j in range(len(keywords[i])):
        if keywords[i][j] not in keywords_list and keywords[i][j] in key:
            keywords_list.append(keywords[i][j])
            keywords_year.append(pub_year[i])
            node_size.append(key[keywords[i][j]])
  
##画个桌面备用 
plt.figure(figsize=(10,6),dpi=300)         

xz = range(1991,2023)
plt.xticks(xz)
plt.yticks([])
plt.grid(axis="x",zorder=0)
w,e=plt.xticks()
plt.setp(e,rotation=60)

ax=plt.gca()  #gca:get current axis得到当前轴
#设置图片的右边框和上边框为不显示
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')

##对数据进行画图，y轴分开，以防撞车
length = 1991
y=0
jump = 6
for i in range(len(keywords_list)):
    if keywords_year[i] == length:
        y += jump
        plt.scatter(keywords_year[i],y,s=node_size[i]*2,zorder=100,alpha=0.6)
        plt.annotate(keywords_list[i],xy=(keywords_year[i],y),fontsize=int(np.log(node_size[i])*3.5),zorder=100)
    elif keywords_year[i] > length:
        length = keywords_year[i]
        y = ((keywords_year[i]-1991+jump)*1.2)
        plt.scatter(keywords_year[i],y,s=node_size[i]*2,zorder=100,alpha=0.6)
        plt.annotate(keywords_list[i],xy=(keywords_year[i],y),fontsize=int(np.log(node_size[i])*3.5),zorder=100)
        continue

#调字体大小 fontsize=int(np.log(node_size[i]))
        


        
            
        
        