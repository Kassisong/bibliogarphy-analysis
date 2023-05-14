#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 08:56:33 2022

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

data = load_csv()

print(len(data))

pub_year = list(data[:,46])

keywords = list(data[:,19])
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
            if 'pulsars' in a1 and 'pulsars: general' not in a1:   
                a1 = a1.replace('pulsars','pulsars: general')
            if 'pulsar' in a1 and 'pulsars: general' not in a1:   
                a1 = a1.replace('pulsar', 'pulsars: general')
            if 'radio pulsars: general' in a1:
                a1 = a1.replace('radio pulsars: general','pulsars: general')
            
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
            if 'neutron star' in a1 and 'neutron stars' not in a1:   
                a1 = a1.replace('neutron star', 'neutron stars')
                
            if 'data analysis' in a1 and 'methods: data analysis' not in a1:   
                a1 = a1.replace('data analysis', 'methods: data analysis')   
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
            if 'accretion disks' in a1 and 'accretion: accretion disks' not in a1:
                a1 = a1.replace('accretion disks','accretion: accretion disks')
            if 'globular star clusters' in a1:
                a1 = a1.replace('globular star clusters','globular clusters')
                
                
                
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
            if 'astronomical observations gamma-ray' in a1:
                a1 = a1.replace('astronomical observations gamma-ray','astronomical observations')
                
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


#读数据 统计词频并转为字典（字典用于绘云图）
key = frequency(keywords_set,86)
w = key.to_dict()

ww = sorted(w.items(), key=lambda x: x[0])
for i in range(len(ww)):
    print(ww[i])

# #根据词频绘云图
# word_cloud = wc.WordCloud(background_color='white',     #背景颜色
#                           scale=10,                     #精细度
#                           random_state=50)              #设置随机生成状态，即多少种配色方案
# word_cloud.fit_words(w)
# word_cloud.to_file("a.png")

color_list=['#CD853F','#DC143C','#00FF7F','#FF6347','#8B008B','#00FFFF','#0000FF','#8B0000','#FF8C00',
            '#1E90FF','#00FF00','#FFD700','#008080','#008B8B','#8A2BE2','#228B22','#FA8072','#808080']

#调用
from matplotlib import colors
colormap=colors.ListedColormap(color_list)

wordcloud = wc.WordCloud(background_color='white',
                         scale=10,
                      max_words = 200,
                      max_font_size = 80,
                      contour_width = 4,
                      colormap=colormap,
                      random_state=50)
wordcloud.fit_words(w)
wordcloud.to_file('Alice_词云图.png')

