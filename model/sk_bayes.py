import pandas as pd
import numpy as np

print("正在加载评论数据。。。")
data = pd.read_csv("./t_comment_detail.csv", usecols=['content', 'rating'])

print(data.info)

data = data.values # 评论文本数据 类别数据（好评/中评/差评）
stopwords_path = './stopwords/hit_stopwords.txt'
stopwords = open(stopwords_path).read().split('\n')

import jieba
def cut(sentence):
  return [token for token in jieba.lcut(sentence) if token not in stopwords]

import torchtext
import torch
#声明一个Field对象，对象里面填的就是需要对文本进行哪些操作，比如这里lower=True英文大写转小写,tokenize=cut对于文本分词采用之前定义好的cut函数，sequence=True表示输入的是一个sequence类型的数据，还有其他更多操作可以参考文档
TEXT = torchtext.data.Field(sequential=True,lower=True,tokenize=cut)
#声明一个标签的LabelField对象，sequential=False表示标签不是sequence，dtype=torch.int64标签转化成整形
LABEL = torchtext.data.LabelField(sequential=False, dtype=torch.int64)
