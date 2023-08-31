import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_csv(dataPath = "23.06.21data filtration.xls"):
    data =pd.read_excel(dataPath) #返回的是DataFrame变量
    cols = data.columns #返回全部列名
    dimensison = data.shape #返回数据的格式，数组，（行数，列数）
    # data.values #返回底层的numpy数据
    row_data = np.array(data.values)#转化为矩阵
    return row_data

#绘制论文发表年份图[折线图]
def publish_count(pub_year,Arttype):
    x = range(1968,2023)
    
    article_counts = {}
    meet_paper_counts = {}
    
    for i in range(len(pub_year)):
        year = pub_year[i]
        if 'Article' in Arttype[i] :
            article_counts[year] = article_counts.get(year, 0) + 1
        elif 'Paper' in Arttype[i] :
            meet_paper_counts[year] = meet_paper_counts.get(year, 0) + 1
    
    pub_num = []
    for i in range(1968,2023):
        pub_num.append(pub_year.count(i))
    
    sorted_years = sorted(set(pub_year))
    
    #绘图以及调格式
    plt.figure(figsize=(16,6))
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"
    
    plt.plot(sorted_years, [article_counts.get(year, 0) for year in sorted_years], 'o--',label='Article',color='red')
    plt.plot(sorted_years, [meet_paper_counts.get(year, 0) for year in sorted_years],'o--', label='Proceedings Paper',color='black')
    plt.scatter(x,pub_num,color='skyblue',label='Total')
    plt.plot(x,pub_num,'.-',color='skyblue')
    xz = range(1968,2023)
    yz = range(0,60,5)
    plt.xticks(xz)
    plt.yticks(yz)
    plt.grid(axis="y")
    w,e=plt.xticks()
    plt.setp(e,rotation=60)
    plt.xlabel('Year')
    plt.ylabel('Public Number')
    plt.legend()
    plt.savefig('1-1.eps', format='eps',bbox_inches='tight')



if __name__ == '__main__':
    data = load_csv()
    pub_year = list(data[:,46])
    Arttype = list(data[:,13])
    publish_count(pub_year,Arttype)
    
