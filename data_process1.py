import pandas as pd
import re
import jieba
import random


def data_process1():  # 分类数据预处理
    file1 = '附件2.xlsx'
    file2 = 'D:/programs/zhihuizhengwu/newdict.txt'
    file3 = 'D:/programs/zhihuizhengwu/stopword.txt'
    data = pd.read_excel(file1)
    data = pd.DataFrame(data, columns=['留言主题','一级分类'])
    data.columns = ['message', 'label']
    data['label_id'] = data['label'].factorize()[0]  # 一级分类标签化
    label_id_df = data[['label', 'label_id']].drop_duplicates().sort_values('label_id').reset_index(drop=True)  # 生成标签表格
    data = data['message'].drop_duplicates()
    data=data.astype(str)
    data_cut = data.apply(lambda x: re.sub('[A-Z0-9]', '', x))  # 去除字母和数字
    jieba.load_userdict(file2)
    data_cut = data_cut.apply(lambda x: jieba.lcut(x))  # 中文分词
    stopWords = pd.read_csv(file3, encoding='utf-8', sep='winner', header=None)
    stopWords = list(stopWords.iloc[:, 0])
    data_after_stop = data_cut.apply(lambda x: [i for i in x if i not in stopWords])  # 去除停用词
    label_id = data.loc[data_after_stop.index, 'label_id']
    adata = data_after_stop.apply(lambda x: ' '.join(x))

    return adata,label_id,label_id_df


def data_process2():  # 聚类数据预处理
    file2 = 'D:/programs/zhihuizhengwu/newdict.txt'
    file4 = '附件2（测试数据）.xlsx'
    file5 = 'D:/programs/zhihuizhengwu/stopword.txt'

    data = pd.read_excel(file4)
    data_t = pd.DataFrame(data, columns=['留言主题'])
    data_cut = data_t['留言主题'].drop_duplicates()
    list_ = data_cut.to_list()
    jieba.load_userdict(file2)
    stopWords = pd.read_csv(file5, encoding='utf-8', sep='winner', header=None)
    stopWords = list(stopWords.iloc[:, 0])
    sentences_cut = []
    for ele in list_:
        cuts = re.sub('[A-Za-z0-9]', '', ele)  # 去除字母
        cuts = jieba.cut(cuts, cut_all=False)  # 中文分词
        new_cuts = []
        for cut in cuts:
            if (cut not in stopWords) and (len(cut) != 1):
                new_cuts.append(cut)
        res = ' '.join(new_cuts)
        if res!= '':
            sentences_cut.append(res)
        else:
            a = range(100)
            sentences_cut.append(str(random.sample(a, 3))) # 若文本处理后为空，则生成随机字符串数组参加聚类
    sentences = sentences_cut
    return sentences
