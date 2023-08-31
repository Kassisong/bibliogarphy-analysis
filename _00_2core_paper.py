import pandas as pd
import numpy as np
import statistics

def load_csv(dataPath="23.06.21data filtration.xls"):
    data =pd.read_excel(dataPath) #返回的是DataFrame变量
    cols = data.columns #返回全部列名
    dimensison = data.shape #返回数据的格式，数组，（行数，列数）
    # data.values #返回底层的numpy数据
    row_data = np.array(data.values)#转化为矩阵
    return row_data

# #筛选高被引论文
def select():
    data = load_csv()
    print('total paper:',len(data))
    #读取论文被引数
    pub_year = list(data[:,46])
    paper = []  
    for i in range(1968,2023):
        paper_temp = []
        for j in range(len(pub_year)):
            if pub_year[j] == i:
                paper_temp.append(data[j])
        paper_temp = np.array(paper_temp)#转数据以便排序
        ref_temp = paper_temp[:,33]#找引用量
    
        median = statistics.median(ref_temp)
        for j in range(len(ref_temp)):
            if ref_temp[j]>median:
                paper.append(paper_temp[j])
    paper = np.array(paper)
    print('core paper',len(paper))
    return paper

if __name__ == '__main__':
    select()
