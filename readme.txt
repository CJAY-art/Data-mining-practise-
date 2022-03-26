1.附件清单：

classification_model.m文件：训练后保存的分类模型
data_enhancement.py:通过网络爬虫，回译留言进行数据增强的程序文件
data_process.py:数据预处理程序文件，包括分类数据预处理和聚类数据预处理两部分
model.py：分类模型训练及效果评估程序文件
thermal_evaluation.py:聚类及热度评价程序文件
response_evaluation.py:答复意见评价程序文件
newdict.txt:特定留言分词文本文件
stopword.txt,stopword1.txt:分别是分类留言文本的停用词和聚类文本留言的停用词
data_enhancement.xlsx:回译得到的增强数据
答复意见评价表.xlsx
热点问题表.xlsx
热点问题留言明细表.xlsx

2.程序内函数参数说明：
baidu_translate(content, from_lang, to_lang):传入字符串，源语言，目标语言；传出翻译后的字符串
back_translate( content, from_lang, to_lang):传入字符串，源语言，目标语言；传出回译后的字符串
data_process1():传出处理后的文本和标签数据，标签表格，datafram格式
data_process2():传出留言预处理后的文本列表
agg_cluster(sentences, cluster):传入文本列表和聚类数，传出聚类标签
get_main(item):传入文本，传出留言描述和命名实体
get_inte(item):传入文本，传出完整性值
get_rati(item):传入文本，传出可解释性值
get_timel(item1, item2):传入留言文本和答复文本，传出及时性值
get_real(item1, item2):传入留言文本和答复文本，传出相关性值


