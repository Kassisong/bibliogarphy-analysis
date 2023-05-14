#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:54:39 2023

@author: songyining
"""

import numpy as np
np.set_printoptions(suppress=True)#不已科学记数法输出

from _00_2core_paper import select

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

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



def countIdf(corpus):
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    return weight


author,author_split = author()
title_set = list(data[:,8])
vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
tfidf=transformer.fit_transform(vectorizer.fit_transform(author))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重 




n_clusters=3
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
    


