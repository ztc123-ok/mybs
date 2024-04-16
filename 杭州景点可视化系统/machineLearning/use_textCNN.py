import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset,DataLoader
from tqdm import tqdm
from collections import Counter
import torch.nn as nn
import re
import emoji
import jieba
import json
import pymysql
import csv

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

# 读取数据
def read_data(sight_id,num = None):
    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",charset="utf8")
    cursor = connect.cursor()

    if num == -1:
        sql = "select id,comments from xc_comments_timesort where sight_id = {} and (positive IS NULL OR positive = '')".format(sight_id)
    else:
        sql = "select id,comments from xc_comments_timesort where sight_id = {}".format(sight_id)
    cursor.execute(sql)
    rest = cursor.fetchall()
    data = [row[1] for row in rest]
    labels = [row[0] for row in rest]  # 记录评论id
    cursor.close()
    connect.close()

    texts = data
    #texts = split_comments(data,num)

    return texts,labels

def split_comments(comments,num = None):
    texts = [] #评论
    stop = [] #停用词表

    #file_stop = 'app/machineLearning/hit_stopwords.txt'  # 停用词表
    with open(file_stop, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()  # lines是list类型
        for line in lines:
            lline = line.strip()  # line 是str类型,strip 去掉\n换行符
            stop.append(lline)  # 将stop 是列表形式
    print("stop[]:", stop[:20])

    for comment in comments[:num]:
        words = []  # 存放切词后、去除停用词后的句子词组
        comment = clean(comment)
        # 使用jieba对评论进行分词
        for word in jieba.lcut(comment):
            # 若切出来的词语 不属于停用词表， 加入词组中
            if word not in stop:
                words.append(word)
        texts.append(words)
    return texts

def update_possitive(id,type):
    # print("正在更新评论情感",id,type)
    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                                           charset="utf8")
    cursor = connect.cursor()
    update_topic = "UPDATE xc_comments_timesort SET positive = '{}' where id = {}".format(type,id)
    cursor.execute(update_topic)
    connect.commit()

    cursor.close()
    connect.close()

class TextDataset(Dataset):
    def __init__(self,all_text,all_label,word_2_index,max_len):
        self.all_text = all_text
        self.all_label = all_label
        self.word_2_index = word_2_index
        self.max_len = max_len
    def __getitem__(self,index):
        text = self.all_text[index][:self.max_len]
        label = int(self.all_label[index])

        # 获取字索引，将句子转换成索引表
        text_idx = [self.word_2_index.get(i,1) for i in text]
        # 不够填充
        text_idx = text_idx + [0] * (self.max_len - len(text_idx))
        # 构建数据集
        text_idx = torch.tensor(text_idx).unsqueeze(dim=0) #增加一个维度

        text_idx = torch.tensor(text_idx)
        return text_idx,label
    def __len__(self):
        return len(self.all_text)

def doTextCNN(comments,labels):
    # print("进行TextCNN评论数：",len(comments))

    texts = split_comments(comments)

    max_len = 20  # 超参数，一个句子最大字数
    batch_size = 10  # 超参数，一次处理多少个句子
    # 使用GPU 预测
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # model_pt = 'app/machineLearning/textCNN.pt'
    mymodel = torch.load(model_pt)
    tf = open(tf_json, "r")
    word_2_index = json.load(tf)
    print("字典长度：",len(word_2_index))
    tf.close()
    #print(word_2_index)
    test_dataset = TextDataset(texts,labels,word_2_index,max_len)
    test_loader = DataLoader(test_dataset, batch_size, shuffle=False)

    # mymodel = torch.load('app/machineLearning/textCNN.pt')
    mymodel.to(device)
    results = []

    for batch_idx, batch_label in test_loader:
        batch_idx = batch_idx.to(device)
        batch_label = batch_label.to(device)
        pre = mymodel.forward(batch_idx)
        data_list = pre.tolist()
        batch_label = batch_label.tolist()
        #print(pre)
        print(batch_label)
        for id,item in zip(batch_label,data_list):
            if int(item) == 1:
                type = "好评"
                #print("好评")
            elif int(item) == 0:
                type = "差评"
                #print("差评")
            results.append(type)
    return results

class Block(nn.Module):
    def __init__(self,kernel_s,embedding_num,max_len,hidden_num):
        super().__init__()
        # 卷积模块
        # 1句话*通道为1*每句话7个词*每个词向量维度是5  [1 * 1 * 7 * 5](batch * in_channel * sentence_len * emb_num)
        # 如果做图片通道为3，对应rgb三色
        self.cnn = nn.Conv2d(in_channels=1,out_channels=hidden_num,kernel_size=(kernel_s,embedding_num))
        # 激活函数（可超参调整）
        self.act = nn.ReLU()
        # 从池中取一个最大值（你需要计算出池的大小）
        self.mxp = nn.MaxPool1d(kernel_size=(max_len-kernel_s+1))

    def forward(self,batch_emb):    #输入维度 [1 * 1 * 7 * 5]
        c = self.cnn.forward(batch_emb)
        a = self.act.forward(c)
        a = a.squeeze(dim=-1) # 去除一个维度
        m = self.mxp.forward(a)
        m = m.squeeze(dim=-1) # 去除一个维度
        return m

class TextCNNModel(nn.Module):
    def __init__(self,emb_matrix,max_len,class_num,hidden_num):
        super().__init__()
        self.emb_num = emb_matrix.weight.shape[1] # 词的维度
        # block的个数也可以作为超参数
        self.block1 = Block(2,self.emb_num,max_len,hidden_num)# 2*5的卷->6*1
        self.block2 = Block(3,self.emb_num,max_len,hidden_num)# 3*5的卷->5*1
        self.block3 = Block(4,self.emb_num,max_len,hidden_num)# 4*5的卷->4*1
        #self.block4 = Block(5, self.emb_num, max_len, hidden_num)  # 4*5的卷->4*1

        self.emb_matrix = emb_matrix

        self.classifier = nn.Linear(hidden_num * 3,class_num) # 2 * 3
        self.weight = torch.tensor([1,2],dtype=torch.float) # 差评，好评
        self.loss_fun = nn.CrossEntropyLoss(weight=self.weight)
        # self.loss_fun = nn.CrossEntropyLoss()

    def forward(self,batch_idx,batch_label=None):
        batch_emb = self.emb_matrix(batch_idx)
        b1_result = self.block1.forward(batch_emb)
        b2_result = self.block2.forward(batch_emb)
        b3_result = self.block3.forward(batch_emb)
        #b4_result = self.block4.forward(batch_emb)

        # 最大池化拼接用于最后分类
        feature = torch.cat([b1_result,b2_result,b3_result],dim=1) # 1 * 6 : [ batch * ( 3 * 2 ) ]
        pre = self.classifier(feature)

        if batch_label is not None:
            loss = self.loss_fun(pre,batch_label)
            return loss
        else:
            # 预测值最大下标返回（概率）
            return torch.argmax(pre,dim=-1)

# file_stop = 'app/machineLearning/hit_stopwords.txt'   # 停用词表
# tf_json = "app/machineLearning/word_2_index.json"
# model_pt = 'app/machineLearning/textCNN.pt'
file_stop = 'hit_stopwords.txt'   # 停用词表
tf_json = "word_2_index.json"
model_pt = 'textCNN.pt'

def textCNNTask(machine_type):
    global file_stop
    global tf_json
    global model_pt
    file_stop = "machineLearning/hit_stopwords.txt"
    tf_json = 'machineLearning/word_2_index.json'
    model_pt = 'machineLearning/textCNN.pt'
    # my_list = ['1']
    my_list = list(range(1, 1861))
    for sight_id in my_list:
        print("标注景点：",sight_id)
        sight_id = str(sight_id)

        if machine_type == 1:
            texts, labels = read_data(sight_id,-1)
        elif machine_type == 2:
            texts, labels = read_data(sight_id)
        elif machine_type == 3:
            return
        print(len(texts))
        results = doTextCNN(texts, labels)
        for i in range(len(texts)):
            update_possitive(labels[i], results[i])

def textCNNOne(sight_id):
    global file_stop
    global tf_json
    global model_pt
    file_stop = "machineLearning/hit_stopwords.txt"
    tf_json = 'machineLearning/word_2_index.json'
    model_pt = 'machineLearning/textCNN.pt'
    # my_list = ['24']
    my_list = list(sight_id)
    for sight_id in my_list:
        print("标注景点：",sight_id)
        sight_id = str(sight_id)

        texts, labels = read_data(sight_id)
        print(len(texts))
        results = doTextCNN(texts, labels)
        for i in range(len(texts)):
            update_possitive(labels[i], results[i])

if __name__ == "__main__":
    # my_list = ['24']
    my_list = list(range(1, 1861))
    for sight_id in my_list:
        print("标注景点：",sight_id)
        sight_id = str(sight_id)

        texts, labels = read_data(sight_id)
        print(len(texts))
        results = doTextCNN(texts, labels)
        for i in range(len(texts)):
            update_possitive(labels[i], results[i])