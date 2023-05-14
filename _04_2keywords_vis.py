#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 20:51:34 2023

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

def keywords():
    data = load_csv()
    
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
    return keywords_set

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


#step2建立初始共现矩阵
def build_matrix(set_word):
    edge = len(set_word) + 1  # 建立矩阵，矩阵的高度和宽度为关键词集合的长度+1
    '''matrix = np.zeros((edge, edge), dtype=str)'''  # 另一种初始化方法
    matrix = [[0 for j in range(edge)] for i in range(edge)]  # 初始化矩阵
    matrix[0][1:] = np.array(set_word)
    matrix = list(map(list, zip(*matrix)))
    matrix[0][1:] = np.array(set_word)  # 赋值矩阵的第一行与第一列
    return matrix


#计算各个关键词关连共现次数，并绘制共现矩阵 【参数：原始数据，统计数据频率】
def count_matrix(O_data, N_data):
    matrix = build_matrix(N_data)
    for row in range(1, len(matrix)):
        # 遍历矩阵第一行，跳过下标为0的元素
        for col in range(1, len(matrix)):
            # 遍历矩阵第一列，跳过下标为0的元素
            # 实际上就是为了跳过matrix中下标为[0][0]的元素，因为[0][0]为空，不为关键词
            if matrix[0][row] == matrix[col][0]:
                # 如果取出的行关键词和取出的列关键词相同，则其对应的共现次数为0，即矩阵对角线为0
                matrix[col][row] = 0
            else:
                counter = 0  # 初始化计数器
                for ech in O_data:
                    # 遍历格式化后的原始数据，让取出的行关键词和取出的列关键词进行组合，
                    # 再放到每条原始数据中查询
                    if N_data.index[row-1] in ech and N_data.index[col-1] in ech:
                        counter += 1
                    else:
                        continue
                matrix[col][row] = int(counter)
    return matrix

#step2矩阵正则化[用于绘制关系图线的粗细]
def regular(O_data, N_data):
    Mat = count_matrix(O_data, N_data)
    #group_Mat = Mat(country, country_num)
    regular_num = max(max(Mat))
    regular = Mat/regular_num
    return regular
 

#step4绘制共现矩阵
#输入值：自数据集各数据出现频率；对应共现矩阵；正则化后共现举证
def coapp_map(data_freq,weight):
    plt.figure(figsize=(16,12),dpi=300)
    G = nx.Graph()
    #加边
    for i in range(2,len(data_freq)):
        for j in range(i+1,len(data_freq)):
            if weight[i+1][j+1] > 0:
                G.add_edge(data_freq.index[i],data_freq.index[j], weight=weight[i+1][j+1])
    
    # 节点位置
    #pos = nx.random_layout(G)
    pos=nx.spring_layout(G)
    #pos=nx.circular_layout(G)
    # pos=nx.kamada_kawai_layout(G)
    
    #中心度
    Gdegree=nx.degree(G)
    Gdegree=dict(Gdegree)
    Gdegree=pd.DataFrame({'name':list(Gdegree.keys()),'degree':list(Gdegree.values())})
    # 首先画出节点位置
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=Gdegree.degree * 50,alpha=0.7)
    
    #根据出现频次绘制线的粗细   
    for i in range(0,11):
        edge = [(u,v) for (u,v,d) in G.edges(data=True) if (d['weight']<i/10)&(d['weight']>=i/10-0.1)]
        nx.draw_networkx_edges(G, pos, edgelist=edge,
                                width = i*2, alpha = 0.5, edge_color = '#F08080')
    
    # labels标签定义
    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif')
    plt.axis('off')
    plt.savefig('fig.png', bbox_inches='tight')
    return ()

if __name__ == '__main__':
    keywords_set = keywords()
    key = frequency(keywords_set,61)
    weight = regular(keywords_set,key)
    draw_author = coapp_map(key,weight)

