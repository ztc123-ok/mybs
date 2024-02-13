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
        elif comment[1] == '中评':
            comment[1] = '0'
        elif comment[1] == '差评':
            comment[1] = '0'
        labels.append(comment[1])

    return texts,labels

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

if __name__ == "__main__":
    # 测试所保存的模型
    #data_path = "comment.csv"
    data_path = "test.csv"
    texts,labels = read_data(data_path)

    max_len = 20  # 超参数，一个句子最大字数
    batch_size = 10  # 超参数，一次处理多少个句子
    # 使用GPU 预测
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    tf = open("word_2_index.json", "r")
    word_2_index = json.load(tf)
    tf.close()
    print(word_2_index)
    test_dataset = TextDataset(texts,labels,word_2_index,max_len)
    test_loader = DataLoader(test_dataset, batch_size, shuffle=False)

    from textCNN import TextCNNModel,Block
    model = torch.load('textCNN.pt').to(device)
    right_num = 0
    for batch_idx, batch_label in test_loader:
        batch_idx = batch_idx.to(device)
        batch_label = batch_label.to(device)
        pre = model.forward(batch_idx)
        print(pre)
        right_num += int(torch.sum(pre == batch_label))

    print(right_num)
    print(f"acc = {right_num / len(texts) * 100:.2f}%")
