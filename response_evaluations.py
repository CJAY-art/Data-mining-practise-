from pyhanlp import *
import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer

file = 'D:/programs/zhihuizhengwu/附件4.0.xlsx'
countVectorizer = CountVectorizer()
data = pd.read_excel(file)
data = pd.DataFrame(data, columns=['留言时间', '留言详情', '答复意见', '答复时间'])
TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")  # textrank模型加载


# 计算完整性
def get_inte(item):
    i = 0
    if re.findall(r'您好|你好', item):
        i = i+1
    if re.findall(r'答复|回复|：', item):
        i = i+1
    if re.findall(r'谢', item):
        i = i+1
    return i


# 计算可解释性
def get_rati(item):
    ra=0
    if re.findall(r'根据|依照|按照|参照|由', item) and re.findall(r'《|》', item):
        ra=1
    return ra


# 计算及时性
def get_timel(item1, item2):
    time1=pd.to_datetime(item1)
    time2=pd.to_datetime(item2)
    if (time2-time1).days <= 14:
        return 1
    else:
        return 0


# # 计算相关性
def get_real(item1, item2):
    sentences=[]
    for item in item1, item2:
        keywords = str(HanLP.extractKeyword(item, 6))   # textrank提取关键词
        sentences.append(keywords)
    vector = countVectorizer.fit_transform(sentences)
    vector = vector.toarray()  # 得到关键词频矩阵
    rea = vector[0]*vector[1]  # 向量位与运算
    # 判断是否有关键词重叠
    if sum(rea) != 0:
        return 1
    else:
        return 0

if __name__ == "__main__":
    rela = []  # 相关性
    inte = []  # 完整性
    rati = []  # 可解释性
    timel = []  # 及时性
    avera = []  # 综合质量

    for index, item in data.iterrows():  # 遍历留言答复计算相关信息
        rela.append((get_real(item['留言详情'], item['答复意见'])))
        inte.append(get_inte(item['答复意见']))
        rati.append((get_rati(item['答复意见'])))
        timel.append(get_timel(item['留言时间'], item['答复时间']))

    data['相关性']=rela
    data['完整性']=(np.array(inte)/3).tolist()
    data['可解释性']=rati
    data['及时性']=timel
    quality=[]  # 存储质量数
    for index, item in data.iterrows():
        qual=(item[4]*4+item[7]*3+inte[6]*2+item[5]*1)/10  # 加权求和再除以权值之和为质量数
        if qual>=0.8:
            quality.append('高')
        elif qual<0.8 and qual>=0.6:
            quality.append('中')
        else:
            quality.append('低')

    data['综合质量']=quality

    writer = pd.ExcelWriter('答复意见评价表.xlsx')
    data.to_excel(writer,index=None)
    writer.save()