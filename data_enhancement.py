import http.client
import hashlib
import json
import urllib
import random
import pandas as pd


def baidu_translate(content, from_lang, to_lang):  # 百度翻译数据传输
    appid = '20200410000416323'
    secretKey = '53ROzERbefgoONbkRX2b'

    q = content
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = '/api/trans/vip/translate'
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        # 获得返回的结果，结果为json格式
        jsonResponse = response.read().decode("utf-8")
        # 将json格式的结果转换字典结构
        js = json.loads(jsonResponse)
        # 取得翻译后的文本结果
        dst = js["trans_result"][0]["dst"]
        return dst
    finally:
        if httpClient:
            httpClient.close()


def back_translate( content, from_lang, to_lang) : # 回译处理
    temp_content=''
    result_content=''
    try:
        # 将原始语种翻译成另外一种语言
        temp_content = baidu_translate(content, from_lang, to_lang)
        # 往回翻译
        result_content = baidu_translate(temp_content, to_lang, from_lang)
        # 存储翻译结果
    except Exception as e:
        print("Error", e)
    return result_content


if __name__ == "__main__":  # 数据增强

    lang = ['en', 'kor', 'jp']
    file1 = 'D:/programs/zhihuizhengwu/附件2.xlsx'
    data = pd.read_excel(file1, header=0, usecols=[2, 5])
    data1 = data[data['一级标签'].values == '环境保护']  # *2
    data2 = data[data['一级标签'].values == '交通运输']  # *3
    data3 = data[data['一级标签'].values == '商贸旅游']  # *2
    data4 = data[data['一级标签'].values == '卫生计生']  # *2
    l1=len(data1)
    l2=len(data2)
    l3=len(data3)
    l4=len(data4)

    df1 = pd.DataFrame(columns=['留言主题'])
    df2 = pd.DataFrame(columns=['留言主题'])
    df3 = pd.DataFrame(columns=['留言主题'])
    df4 = pd.DataFrame(columns=['留言主题'])
    i=0
    for index, row in data1.iterrows():
        content = row['留言主题']
        results1 = back_translate(content, "zh", lang[0])
        results2 = back_translate(content, "zh", lang[1])
        df1 = df1.append([{'留言主题': results1}], ignore_index=True)
        df1 = df1.append([{'留言主题': results2}], ignore_index=True)
        i=i+1
        print("\r1:{:}/{:}".format(i, l1), end='')
    i=0
    for index, row in data2.iterrows():
        content = row['留言主题']
        results1 = back_translate(content, "zh", lang[0])
        results2 = back_translate(content, "zh", lang[1])
        results3 = back_translate(content, "zh", lang[2])
        df2 = df2.append([{'留言主题': [results1]}], ignore_index=True)
        df2 = df2.append([{'留言主题': [results2]}], ignore_index=True)
        df2 = df2.append([{'留言主题': [results3]}], ignore_index=True)
        i = i + 1
        print("\r2:{:}/{:}".format(i, l2), end='')
    i=0
    for index, row in data3.iterrows():
        content = row['留言主题']
        results1 = back_translate(content, "zh", lang[0])
        results2 = back_translate(content, "zh", lang[1])
        df3 = df3.append([{'留言主题': [results1]}], ignore_index=True)
        df3 = df3.append([{'留言主题': [results2]}], ignore_index=True)
        i = i + 1
        print("\r3:{:}/{:}".format(i, l3), end='')
    i=0
    for index, row in data4.iterrows():
        content = row['留言主题']
        results1 = back_translate(content, "zh", lang[0])
        results2 = back_translate(content, "zh", lang[1])
        df4 = df4.append([{'留言主题': [results1]}], ignore_index=True)
        df4 = df4.append([{'留言主题': [results2]}], ignore_index=True)
        i = i + 1
        print("\r4:{:}/{:}".format(i, l4), end='')

    writer = pd.ExcelWriter('date_enhancement.xlsx')
    df1.to_excel(writer)
    df2.to_excel(writer, startrow=len(df1)+5)
    df3.to_excel(writer, startrow=len(df1)+len(df2)+10)
    df4.to_excel(writer, startrow=len(df1)+len(df2)+len(df3)+15)

    writer.save()
