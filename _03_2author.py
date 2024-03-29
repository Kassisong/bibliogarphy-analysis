import numpy as np
np.set_printoptions(suppress=True)#不已科学记数法输出
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from _00_2core_paper import select

def author():
    data = select()
    print(len(data))
    
    #读取论文作者信息
    author = data[:,1]
    Atype = data[:,13]
    author_set = []
    for i in range(len(author)):
        # if 'Review' not in Atype[i]:
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
        
        a = a.split(';',10000)
        author_set.append(a)
        # else:
        #     continue
    return author_set

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

def frequency_new(data):
    count = [count for sublist in data for count in sublist]
    
    # 创建字典用于存储作者及其出现的频次
    data_freq = {}
    
    # 遍历作者列表并进行计数
    for i in count:
        data_freq[i] = data_freq.get(i, 0) + 1
    data_freq = pd.Series(data_freq)
    data_freq = data_freq.sort_values(ascending=False)
    return data_freq

#step2建立初始共现矩阵
#程序初始第一行&第一列加了个频次数据统计（导致矩阵变成N+1*N+1），存粹为了与可阅读行美观。真实的共现矩阵从第二行开始计算的。
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
    plt.figure(figsize=(30,20))
    G = nx.Graph()
    #加边
    for i in range(len(data_freq)):
        for j in range(i+1,len(data_freq)):
            if weight[i+1][j+1] > 0.05:
                G.add_edge(data_freq.index[i],data_freq.index[j], weight=weight[i+1][j+1])
    
    # 节点位置
    # pos = nx.random_layout(G)
    pos=nx.spring_layout(G)
    # pos=nx.circular_layout(G)
    # pos=nx.shell_layout(G) 
    # pos=nx.spectral_layout(G)
    # pos=nx.kamada_kawai_layout(G)
    
    #中心度
    Gdegree=nx.degree(G)
    Gdegree=dict(Gdegree)
    Gdegree=pd.DataFrame({'name':list(Gdegree.keys()),'degree':list(Gdegree.values())})
    
    
    cent = nx.degree_centrality(G)
    # 首先画出节点位置
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=Gdegree.degree * 50,alpha=0.7)
    
    #根据出现频次绘制线的粗细   
    for i in range(0,11):
        edge = [(u,v) for (u,v,d) in G.edges(data=True) if (d['weight']<i/20)&(d['weight']>=i/20-0.05)]
        nx.draw_networkx_edges(G, pos, edgelist=edge,
                                width = i, alpha = i/10, edge_color = '#F08080')
    
    #labels标签定义
    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif')
    plt.axis('off')
    plt.savefig('author_net12_5.png', bbox_inches='tight')
    return ()



if __name__ == '__main__':
    #绘制作者关系图
    author_set = author()
    print(len(author_set))
    author_numO = frequency_new(author_set)
    author_num = author_numO[:87]
    weight = regular(author_set,author_num)
    draw_author = coapp_map(author_num,weight)
