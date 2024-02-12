import pandas as pd
import numpy as np
import jieba
from sklearn.model_selection import train_test_split
import emoji
import re
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

print("正在加载评论数据。。。")
# 好评：40613 中评：2472 差评：530
data = pd.read_csv("./t_comment_detail.csv", usecols=['content', 'rating'])
data = data.values # 评论文本数据 类别数据（好评/差评）
# print("data[:2]:",data[:2])

print("正在加载停用词。。。")
stop = [] # 停用词表
file_stop = './stopwords/hit_stopwords.txt'  # 停用词表
with open(file_stop, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()  # lines是list类型
    for line in lines:
        lline = line.strip()  # line 是str类型,strip 去掉\n换行符
        stop.append(lline)  # 将stop 是列表形式
print("stop[]:",stop[:20])

dictionary = []  # 定义词典
clear_dataset = []  # 定义清洗后的数据集
for comment in data:
    if comment[1] == '中评':
        comment[1] = '差评'
    words = []  # 存放切词后、去除停用词后的句子词组
    comment[0] = clean(comment[0])
    # 使用jieba对评论进行分词
    for word in jieba.lcut(comment[0]):

        # 若切出来的词语 不属于停用词表， 加入词组中
        if word not in stop:
            words.append(word)

        # 向词典中加入所有未加入的词语
        if word not in dictionary:
            dictionary.append(word)

    # 追加句子词组和对应的标志
    clear_dataset.append([words, comment[1]])
print("词典长度:",len(dictionary))
print("clear_dataset[:2]:",clear_dataset[:2])

from sklearn.model_selection import train_test_split

X = []  # 存放向量化后的评论
y = [y[1] for y in clear_dataset]  # 存放每条评论的类别

# 遍历所有清洗后的评论数据，并将所有评论文本信息转化为向量信息
for clear_data in clear_dataset:

    # 评论信息列表赋值为sentence
    sentence = clear_data[0]

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

X = np.array(X)               #转化为numpy数组，X作为输入项，即评论生成的向量
y = np.array(y)               #转化为numpy数组，y作为输出项，即评论的类别

#X_train，y_train为训练集数据
#X_test,y_test为测试集数据
#使用sklearn库的随即切分函数，将X、y划分为训练集与测试集(0.8:0.2),开启随机混合使每次划分结果不同
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,shuffle=True)

#分别输出训练集的 X, y形状， 测试集的X, y的形状
print('X_train.shape',X_train.shape)
print('y_train.shape',y_train.shape)
print('X_test.shape',X_test.shape)
print('y_test.shape',y_test.shape)

# 欠采样后效果反而不是很好
# from imblearn.under_sampling import RandomUnderSampler
#
# print("Before undersampling: ", Counter(y_train))
#
# # 调用方法进行欠采样
# undersample = RandomUnderSampler(sampling_strategy='majority')
#
# # 获得欠采样后的样本
# X_train, y_train = undersample.fit_resample(X_train, y_train)
#
# # 统计欠采样后的类别占比情况
# print("After undersampling: ", Counter(y_train))

len_dic = len(dictionary)  # 词典的长度，即所有词的长度

good_pro = np.sum(y_train == '好评') / len(X_train)  # 好评率

good_num = 0  # 好评的次数
bad_num = 0  # 差评的次数

# 初始化之所以为 1，是防止P(特征i|类别)中某个为0，导致连乘积为0
good_vec = np.ones(len_dic)  # 向量组，每个值代表好评的次数,初始化全为1
bad_vec = np.ones(len_dic)  # 向量组，每个值代表差评的次数，初始化全为1

for i in range(len(X_train)):

    # 代表的是好评
    if y_train[i] == '好评':
        good_vec += X_train[i]  # 把该评论词语代表的向量,累加到good_vec
        good_num += 1  # 好评次数增加

    # 否则是差评
    else:
        bad_vec += X_train[i]  # 把该评论词语代表的向量,累加到bad_vec
        bad_num += 1  # 差评次数增加

# 取log的原因有二：1、拉普拉斯平滑，防止太小的结果乘积造成下溢。2、log(连乘积)可以转化为 log累加
good_vec_trained = np.log(good_vec / good_num)  # 用于存放所有的 P(特征i|好评)向量，每个值代表一个概率
bad_vec_trained = np.log(bad_vec / bad_num)  # 用于存放所有的 P(特征i|差评)向量，每个值代表一个概率

print('好评率: {}'.format(good_pro))
print('good_vec_trained is: {}'.format(good_vec_trained[:20]))
print('bad_vec_trained is: {}'.format(bad_vec_trained[:20]))

success_count = 0

for i in range(len(X_test)):

    # 代入朴素贝叶斯公式

    # 评论好评的概率
    good_pro_pre = np.sum(X_test[i] * good_vec_trained) + np.log(good_pro)

    # 评论差评的概率
    bad_pro_pre = np.sum(X_test[i] * bad_vec_trained) + np.log(1 - good_pro)

    # 若好评概率大于差评概率
    if good_pro_pre > bad_pro_pre:
        result = '好评'  # 输出好评

    else:
        result = '差评'  # 否则输出差评

    if (y_test[i] == result):  # 若预测答案与真实答案相等，预测正确数量增加
        success_count += 1

    # 保存模型
with open("dictionary.csv", "a", encoding='utf-8') as f:
    f.writelines("good_pro"+","+str(good_pro)+"\n")
    for i in range(len(dictionary)):
        f.writelines(dictionary[i] + "," + str(good_vec_trained[i]) + "," + str(bad_vec_trained[i]) + "\n")

print('朴素贝叶斯模型(bayes)预测的准确度: {}'.format(success_count / len(X_test)))
# best: 0.6657113378424854