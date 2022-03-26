import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from data_process import data_process2
from sklearn.metrics import silhouette_score
from pyhanlp import *


# 层次聚类函数
def agg_cluster(sentences, cluster):
    countVectorizer = CountVectorizer(lowercase=False)
    vector = countVectorizer.fit_transform(sentences)
    vector = vector.toarray()  # 得到词频矩阵

    # 对矩阵中的高频词语加权
    s = []
    leng = np.size(vector, 1)
    for i in range(0, leng):
        s.append(vector[:, i] * (np.sum(vector[:, i])**2))
    s = np.transpose(np.array(s))
    # print(cosine_similarity(s[5].reshape(1, -1), s[6].reshape(1, -1)))

    # 标准化矩阵
    scaler = StandardScaler(with_mean=False)
    sparse_data = scaler.fit_transform(s)

    # 进行聚类
    model = AgglomerativeClustering(n_clusters=cluster, affinity="cosine", linkage='average')
    labels = model.fit_predict(sparse_data)

    return labels  # 返回聚类标签

# 最佳聚类数分析
# sentences=data_process2()
# countVectorizer = CountVectorizer(lowercase=False)
# vector = countVectorizer.fit_transform(sentences)
# vector = vector.toarray()  # 得到词频矩阵
#
# # 对矩阵中的高频词语加权
# s = []
# leng = np.size(vector, 1)
# for i in range(0, leng):
#     s.append(vector[:, i] * (np.sum(vector[:, i])**2))
# s = np.transpose(np.array(s))
# # print(cosine_similarity(s[5].reshape(1, -1), s[6].reshape(1, -1)))
#
# # 标准化矩阵
# scaler = StandardScaler(with_mean=False)
# sparse_data = scaler.fit_transform(s)
# coef = []
# X = range(10, 50, 5)
# for cluster in X:
#     model = AgglomerativeClustering(n_clusters=cluster, affinity="cosine", linkage='average')
#     labels = model.fit_predict(sparse_data)
#     silhouette_avg = 1-silhouette_score(sparse_data, labels, metric='cosine')
#     coef.append(silhouette_avg)
#
# # 中文和负号正常显示
# plt.rcParams['font.sans-serif'] = 'SimHei'
# plt.rcParams['axes.unicode_minus'] = False
# plt.style.use('ggplot')
# plt.plot(X, coef)
# plt.xlabel('簇的个数')
# plt.ylabel('轮廓系数')
# plt.show()


file2 = 'D:/programs/zhihuizhengwu/newdict.txt'
file5 = 'D:/programs/zhihuizhengwu/stopword.txt'

# 加载hanlp命名实体识别模型
ha_model = HanLP.newSegment()
jieba.load_userdict(file2)
stopWords = pd.read_csv(file5, encoding='utf-8', sep='winner', header=None)
stopWords = list(stopWords.iloc[:, 0])


# 命名实体识别（地点人群），及留言描述提取函数
def get_main(item):
    cuts = jieba.cut(item, cut_all=False)
    dictnt=['nit', 'nt', 'nic', 'nis', 'ntc', 'ntcb', 'ntcf', 'ntch', 'nth', 'nto',	'nts',	'ntu', ]
    disc = ''
    m=[]
    for word in cuts:
        if word not in stopWords:
            disc = disc + word
        i = ha_model.seg(word).get(0)
        if str(i.nature) == 'ns'or dictnt.__contains__(str(i.nature)) or (str(i.nature) == 'nnt'or str(i.nature) == 'nnd'or str(i.nature) == 'nx'):
            m.append(word)
    return disc, m


if __name__ == "__main__":
    sentences=data_process2()
    cluster=18
    labels=agg_cluster(sentences, cluster)  # 聚类
    #  根据聚类标签对留言归类排序
    file4 = 'D:/programs/zhihuizhengwu/附件3.0.xlsx'
    data = pd.read_excel(file4)
    data_t = pd.DataFrame(data)
    index = labels.argsort()  # 根据指针排序
    data_t.insert(0, '问题ID', 0)
    for i in range(len(index)):
        data_t.loc[index[i]:index[i], '问题ID'] = [labels[index[i]] + 1]
    data_sort = data_t.sort_values(by='问题ID', ascending=True)

    # 计算每类热度
    temp = {}  # 存储热度
    N = len(data_sort)  # 总留言条数

    for i in range(cluster):
        sup = np.sum(data_sort[data_sort['问题ID'].values == i + 1]['点赞数'])  # 每类点赞数
        opp = np.sum(data_sort[data_sort['问题ID'].values == i + 1]['反对数'])  # 每类反对数
        ni = len(data_sort[data_sort['问题ID'].values == i + 1])  # 每类条数
        if (sup + opp) != 0:
            tem = ni + sup * sup / (sup + opp)  # 热度指标定义
        else:
            tem = ni
        temp[i + 1] = tem

    # 提取热度前5的类别ID并排序
    n = 5
    L = sorted(temp.items(), key=lambda item: item[1], reverse=True)
    L = L[:n]
    dictdata = {}
    for l in L:
        dictdata[l[0]] = l[1]

    keys = list(dictdata.keys())  # 存放类别id
    atemp = list(dictdata.values())  # 存放热度系数
    time = []  # 存放时间范围
    main = []  # 存放地点人群
    disc = []  # 存放问题描述
    rank = [1, 2, 3, 4, 5]  # 标号顺序

    # 提取每类留言的代表信息
    for key in keys:
        dmax = np.max(data_sort[data_sort['问题ID'].values == key]['点赞数'])
        for index, item in data_sort[data_sort['问题ID'].values == key].iterrows():
            if item['点赞数'] == dmax:
                d, m = get_main(item['留言主题'])
                disc.append(d)
                main.append(''.join(m))
                break

    # 每类时间范围提取
    for key in keys:
        timelist = []
        for index, item in data_sort[data_sort['问题ID'].values == key].iterrows():
            timelist.append(pd.to_datetime(item['留言时间']).strftime('%Y/%m/%d'))
        timemax = str(max(timelist))
        timemin = str(min(timelist))
        time.append(timemin + '至' + timemax)

    # 文件保存
    data1 = {"热度排名": rank, '问题ID ': keys, '热度指数': atemp, '地点/人群': main, '问题描述': disc}
    writer1 = pd.ExcelWriter('热点问题表.xlsx')
    writer2 = pd.ExcelWriter('热点问题留言明细表.xlsx')
    data1 = pd.DataFrame(data1)
    data1.to_excel(writer1, index=None)
    data_sort.to_excel(writer2, index=None)
    writer1.save()
    writer2.save()
