#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '杭州景点可视化系统.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

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

# 块由三部分组成：卷积，激活，最大池化
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

if __name__ == '__main__':
    main()
