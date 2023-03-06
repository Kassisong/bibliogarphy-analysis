#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:54:39 2023

@author: songyining
"""

import numpy as np
np.set_printoptions(suppress=True)#不已科学记数法输出
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import networkx as nx
from _00_2core_paper import select

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA

data = select()
print(len(data))

def author():
    #读取论文作者信息
    author = data[:,1]
    author_set = []
    author_split = []
    for i in range(len(author)):
        a = ''.join(str(i) for i in author[i])
        a = a.upper()
        a = a.replace(" ", "")
        a = a.replace('\'', '')
        a = a.replace('-', '')
        a = a.replace('.', '')
        a = a.replace(';',' ')
        b = a.split(';',300)
        author_set.append(a)
        author_split.append(b)
    return author_set,author_split

author,author_split = author()

title_set = list(data[:,8])

def countIdf(corpus):
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    return weight


vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
tfidf=transformer.fit_transform(vectorizer.fit_transform(author))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重 



#word=vectorizer.get_feature_names()#获取词袋模型中的所有词


from sklearn.cluster import KMeans

# cost = []#初始化损失（距离）值
# for i in range(1,200):#尝试不同的K值
#     kmeans = KMeans(n_clusters= i ,init='k-means++', random_state = 0)
#     kmeans.fit(weight)
#     cost.append(kmeans.inertia_)

# #绘制手肘图找到最佳K值
# import matplotlib.pyplot as plt

# hist,ax = plt.subplots()
# plt.plot(range(1,200),cost)
# # plt.title('The Elbow Method')
# ax.set_title('The Elbow Method')
# ax.set_ylabel('Cost')
# plt.show()


n_clusters=16
mykms=KMeans(n_clusters,init='k-means++')
y=mykms.fit_predict(weight)

n_clusters = max(y+1)

f = open('author_cluster__'+str(n_clusters)+'.txt', 'w')
label = []
for i in range(n_clusters):
    label_i=[]
    f.write('Class '+str(i)+'\n')
    for j in range(0,len(y)):
        if y[j]==i:
            label_i.append(title_set[j])
            f.write(str(j)+'    '+title_set[j]+'\n')
            f.flush()
    f.write('\n')
    label.append(label_i)
    


