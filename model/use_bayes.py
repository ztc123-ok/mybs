import pandas as pd
import numpy as np
import jieba
from sklearn.model_selection import train_test_split
import emoji
import re
import csv
from collections import Counter

def clean(list,restr=''):
    # 过滤表情,我还得专门下个emoji的库可还行，数据库字段设utf8mb4好像也行,字段里含有‘和“写sql也会错
    # 谁家取昵称还带表情啊
    try:
        co = re.compile(
            u'['u'\U0001F300-\U0001F64F'u'\U00010000-\U0010ffff' u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55]+')
    except re.error:
        co = re.compile(
            u'('u'\ud83c[\udf00-\udfff]|'u'[\uD800-\uDBFF][\uDC00-\uDFFF]'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+')
    if (isinstance(list, str)):
        list = co.sub(restr, list)
        list = emoji.replace_emoji(list, restr)
        list = list.replace("'", restr)
        list = list.replace('"', restr)
        list = list.replace(' ',restr)
        list = list.replace('\n',restr)
        list = list.replace('\\', restr)
    else:
        for i in range(len(list)):
            list[i] = co.sub(restr, list[i])
            list[i] = emoji.replace_emoji(list[i], restr)
            list[i] = list[i].replace("'", restr)
            list[i] = list[i].replace('"', restr)
            list[i] = list[i].replace(' ',restr)
            list[i] = list[i].replace('\n',restr)
            list[i] = list[i].replace('\\', restr)

    return list

def read_data(data_path,num = None):
    data = pd.read_csv(data_path, usecols=['content', 'rating'])
    data = data.values  # 评论文本数据 类别数据（好评/差评）

    texts = [] #评论
    labels = [] #类别
    stop = [] #停用词表

    file_stop = './stopwords/hit_stopwords.txt'  # 停用词表
    with open(file_stop, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()  # lines是list类型
        for line in lines:
            lline = line.strip()  # line 是str类型,strip 去掉\n换行符
            stop.append(lline)  # 将stop 是列表形式
    print("stop[]:", stop[:20])

    for comment in data[:num]:
        words = []  # 存放切词后、去除停用词后的句子词组
        comment[0] = clean(comment[0])
        # 使用jieba对评论进行分词
        for word in jieba.lcut(comment[0]):
            # 若切出来的词语 不属于停用词表， 加入词组中
            if word not in stop:
                words.append(word)

        texts.append(words)
        if comment[1] == '好评':
            comment[1] = '1'
        elif comment[1] == '差评':
            comment[1] = '0'
        labels.append(comment[1])

    return texts,labels

texts,labels = read_data("./test.csv")

good_vec_trained = []
bad_vec_trained = []
dictionary = []

with open('dictionary.csv', 'r',encoding='utf-8') as file:
    reader = csv.reader(file)
    good_pro = float(next(reader, None)[1])
    for row in reader:
        # 提取需要的两列数据
        dictionary.append(row[0])
        good_vec_trained.append(float(row[1]))
        bad_vec_trained.append(float(row[2]))

good_vec_trained = np.array(good_vec_trained)
bad_vec_trained = np.array(bad_vec_trained)
X = []  # 存放向量化后的评论

for sentence in texts:

    # 首先将每个评论分词列表设置为 (1,5023)的向量，每个向量值为1
    # 一个句子转化为一个向量
    word_2_vec = np.zeros(len(dictionary))

    # 遍历字典，将所有评论分词列表 转化为 向量列表
    for word in sentence:

        # 如果word存在于字典中
        if word in dictionary:
            # 找到该词在字典中的位置
            loc = dictionary.index(word)

            # 此句子对照向量的该位置加1
            word_2_vec[loc] += 1

            # X，即输入句子的特征向量列表，追加新句子向量
    X.append(word_2_vec)


success_count = 0

print(good_vec_trained)
for i in range(len(X)):

    # 代入朴素贝叶斯公式

    # 评论好评的概率
    good_pro_pre = np.sum(X[i] * good_vec_trained) + np.log(good_pro)

    # 评论差评的概率
    bad_pro_pre = np.sum(X[i] * bad_vec_trained) + np.log(1 - good_pro)

    # 若好评概率大于差评概率
    if good_pro_pre > bad_pro_pre:
        result = 1  # 输出好评

    else:
        result = 0  # 否则输出差评
    if (labels[i] == result):  # 若预测答案与真实答案相等，预测正确数量增加
        success_count += 1
    print(result,labels[i])

print('朴素贝叶斯模型(bayes)预测的准确度: {}'.format(success_count / len(X)))