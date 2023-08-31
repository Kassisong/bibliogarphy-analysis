import numpy as np
np.set_printoptions(suppress=True)#不已科学记数法输出
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import re




def load_csv(dataPath = "23.06.21data filtration.xls"):
    data =pd.read_excel(dataPath) #返回的是DataFrame变量
    cols = data.columns #返回全部列名
    dimensison = data.shape #返回数据的格式，数组，（行数，列数）
    # data.values #返回底层的numpy数据
    row_data = np.array(data.values)#转化为矩阵
    return row_data

data = load_csv()
print(len(data))

addresses = data[:,22]
country = []
for i in range(len(addresses)):
    if type(addresses[i]) == float:
        country.append(list('0'))
    else:
        a = ''.join(str(i) for i in addresses[i])
        a = ''.join([i for i in a if not i.isdigit()])              #删除数字
        a = a.title()                                               #首字母大写以匹配筛选
        a = a.strip()
        p = re.compile(r'[[](.*?)[]]', re.S)
        a = re.sub(p,'',a).split(';',100)
        
        a1 = []
        for i in a:
            i = i.strip()
            a2 = i.split(' ',100)
            cou = a2[-1]
            if ',' in cou:
                cou = ''.join(str(i) for i in cou)
                cou = cou.split(',',100)
                cou = cou[-1]
            if 'Al' in cou or 'Ak' in cou or 'Az' in cou or 'Co' in cou or 'Ct' in cou or 'Dc' in cou or 'De' in cou or 'Fl' in cou or 'Ga' in cou:
                cou = 'Usa'
            if 'Hi' in cou or 'Id' in cou or 'Il' in cou or 'Ia' in cou or 'Ks' in cou or 'Ky' in cou or 'La' in cou or 'Md' in cou:
                cou = 'Usa'
            if 'Ma' in cou or 'Mi' in cou or 'Mn' in cou or 'Ms' in cou:
                cou = 'Usa'
            if 'Mt' in cou or 'Nv' in cou or 'Nh' in cou or 'Nj' in cou:
                cou = 'Usa'
            if 'Nm' in cou or 'Ny' in cou or 'Nc' in cou or 'Nd' in cou or 'Oh' in cou:
                cou = 'Usa'
            if 'Ok' in cou or 'Or' in cou or 'Pa' in cou or 'Pr' in cou or 'Ri' in cou or 'Sc' in cou:
                cou = 'Usa'
            if 'Sd' in cou or 'Tn' in cou or 'Tx' in cou or 'Ut' in cou or 'Vt' in cou:
                cou = 'Usa'
            if 'Va' in cou or 'Wa' in cou or 'Wv' in cou or 'Wi' in cou or 'Wy' in cou:
                cou = 'Usa'
            
            if 'Ca' in cou and 'Canada' not in cou:
                cou = 'Usa'
            if 'In' in cou and 'India' not in cou:
                cou = 'Usa'
            if 'Me' in cou and 'Mexico' not in cou:
                cou = 'Usa'
            if 'Mo' in cou and 'Morocco' not in cou:
                cou = 'Usa'
            
            if 'Ger' in cou:
                cou = 'Germany'
            if 'Zealand' in cou:
                cou = 'New Zealand'
            if 'Africa' in cou:
                cou = 'South Africa'
            if 'Republic' in cou:
                cou = 'Czech Republic'
           
            if 'Kong' in cou:
                cou = 'China'
            if 'Taiwan' in cou:
                cou = 'China'
            if 'Macao' in cou:
                cou = 'China'
                
            if cou not in a1:
                a1.append(cou)
        country.append(a1)

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
    plt.figure(figsize=(20,15),dpi=300)
    G = nx.Graph()
    #加边
    for i in range(len(data_freq)):
        for j in range(i+1,len(data_freq)):
            if weight[i+1][j+1] > 0:
                G.add_edge(data_freq.index[i],data_freq.index[j], weight=weight[i+1][j+1])
    
    # 节点位置
    #pos = nx.random_layout(G)
    #pos=nx.spring_layout(G)
    #pos=nx.circular_layout(G)
    pos=nx.kamada_kawai_layout(G)
    
    #中心度
    Gdegree=nx.degree(G)
    Gdegree=dict(Gdegree)
    Gdegree=pd.DataFrame({'name':list(Gdegree.keys()),'degree':list(Gdegree.values())})
    # 首先画出节点位置
    
    nx.draw_networkx_nodes(G, pos, node_size=Gdegree.degree * 100,alpha=0.5)
    
    #根据出现频次绘制线的粗细  
    #color = plt.get_cmap('Reds')(np.linspace(0,1,len(country_num)))
    
    for i in range(1,50):
        edge = [(u,v) for (u,v,d) in G.edges(data=True) if (d['weight']<i/50)&(d['weight']>=i/50-0.02)]
        nx.draw_networkx_edges(G, pos, edgelist=edge,
                               width = i*1.2, edge_color = '#F08080')
    
    # labels标签定义
    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif')
    plt.axis('off')
    plt.savefig('fig.png', bbox_inches='tight')
    return ()

#绘制国家共现图
if __name__ == '__main__':
    country_num = frequency(country,51)
    weight = regular(country,country_num)
    draw_country = coapp_map(country_num,weight)
