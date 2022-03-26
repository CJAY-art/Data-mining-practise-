from data_process import data_process2,data_process1
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import  pandas as pd
from sklearn.externals import joblib
import warnings
import xlwt
import xlrd
from xlutils.copy import copy
warnings.filterwarnings('ignore')


if __name__ == "__main__":
    # adata=data_process1()
    data=data_process2()
    # model = joblib.load("classification _model.m")
    # countVectorizer = CountVectorizer()
    labels=['城乡建设','环境保护','交通运输','教育文体','劳动和社会保障','商贸旅游','卫生计生']
    # data_tr = countVectorizer.fit_transform(adata)
    # X_tr = TfidfTransformer().fit_transform(data_tr.toarray()).toarray()

    # labels_pr = model.predict(X_te)
    # print(labels_pr)
    adata, label_id, label_id_df = data_process1() # 获取数据
    data_tr, data_te, labels_tr, labels_te = train_test_split(adata, label_id, test_size=0.2)   # 数据划分

    countVectorizer = CountVectorizer()
    data_tr = countVectorizer.fit_transform(data_tr)
    X_tr = TfidfTransformer().fit_transform(data_tr.toarray()).toarray()   # 构建tf-idf权重矩阵
    data_te = CountVectorizer(vocabulary=countVectorizer.vocabulary_).fit_transform(data)
    X_te = TfidfTransformer().fit_transform(data_te.toarray()).toarray()
    # data_te = CountVectorizer(vocabulary=countVectorizer.vocabulary_).fit_transform(data_te)
    # X_te = TfidfTransformer().fit_transform(data_te.toarray()).toarray()

    model = LinearSVC()  # 定义线性支持向量机分类器
    model.fit(X_tr, labels_tr)  # 模型训练
    labels_pr = model.predict(X_te)  # 模型预测
    gg=[]

    for label in labels_pr:
        gg.append(labels[label])
    file = '附件2（测试结果）.xlsx'
    file1 = '附件2（测试结果）1.xls'
    rb = xlrd.open_workbook(file)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    for i in range(len(gg)):
        ws.write(i+1, 1, gg[i])
    wb.save(file1)
    # print('accuracy %s' % accuracy_score(labels_pr, labels_te))  # 汇报各分类评估结果
    # print(classification_report(labels_te, labels_pr, target_names=label_id_df['label'].values))

    # conf_mat = confusion_matrix(labels_te, labels_pr)  # 展示判断矩阵
    # fig, ax = plt.subplots(figsize=(10, 8))
    # sns.heatmap(conf_mat, annot=True, fmt='d',
    #             xticklabels=label_id_df.label.values, yticklabels=label_id_df.label.values)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # plt.ylabel('实际结果', fontsize=18)
    # plt.xlabel('预测结果', fontsize=18)
    # plt.show()
    #
    # # 模型保存
    # joblib.dump(model, "classification _model.m")
    # 模型调回

