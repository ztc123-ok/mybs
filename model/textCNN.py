import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset,DataLoader
from tqdm import tqdm
import torch.nn as nn
import re
import emoji
import jieba

data_path = "./t_comment_detail.csv"

#清洗文本数据
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

def build_curpus(train_texts,embedding_num):
    # 将word 对应成数字
    word_2_index = {"<PAD>":0,"<UNK>":1}
    for text in train_texts:
        for word in text:
            word_2_index[word] = word_2_index.get(word,len(word_2_index))
    #words_embedding 通常指的是这样一个嵌入向量矩阵，其中每一行代表词汇表中的一个单词的嵌入向量
    #nn.Embedding用来将一个数字变成一个指定维度的向量,作为模型的第一层,这n维的向量会参与模型训练并且得到更新，从而数字会有一个更好的128维向量的表示
    #这里返回所有数字对应的向量表
    return word_2_index,nn.Embedding(len(word_2_index),embedding_num)

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
        text_idx = [self.word_2_index.get(i,"1") for i in text]
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
    def __init__(self,kernel_s,embedding_num,max_len):
        super().__init__()
        # 卷积模块
        # 1句话*通道为1*每句话7个词*每个词向量维度是5  [1 * 1 * 7 * 5](batch * in_channel * sentence_len * emb_num)
        # 如果做图片通道为3，对应rgb三色
        self.cnn = nn.Conv2d(in_channels=1,out_channels=2,kernel_size=(kernel_s,embedding_num))
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
    def __init__(self,emb_matrix,max_len,class_num):
        super().__init__()
        self.emb_num = emb_matrix.weight.shape[1] # 词的维度
        self.block1 = Block(2,self.emb_num,max_len)# 2*5的卷->6*1
        self.block2 = Block(3,self.emb_num,max_len)# 3*5的卷->5*1
        self.block3 = Block(4,self.emb_num,max_len)# 4*5的卷->4*1

        self.emb_matrix = emb_matrix

        self.classifier = nn.Linear(6,class_num)
        self.loss_fun = nn.CrossEntropyLoss()

    def forward(self,batch_idx,batch_label=None):
        batch_emb = self.emb_matrix(batch_idx)
        b1_result = self.block1.forward(batch_emb)
        b2_result = self.block2.forward(batch_emb)
        b3_result = self.block3.forward(batch_emb)

        # 最大池化拼接用于最后分类
        feature = torch.cat([b1_result,b2_result,b3_result],dim=1) # 1 * 6 : [ batch * ( 3 * 2 ) ]
        pre = self.classifier(feature)

        if batch_label is not None:
            loss = self.loss_fun(pre,batch_label)
            return loss
        else:
            # 预测值最大下标返回（概率）
            return torch.argmax(pre,dim=-1)

if __name__ == "__main__":
    texts,labels = read_data(data_path,3000)

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.20, shuffle=True)

    # 分别输出训练集的 X, y形状， 测试集的X, y的形状
    print(X_train[:5])
    print(y_train[:5])

    embedding = 5
    max_len = 7
    batch_size = 1
    epoch = 10
    lr = 0.001
    class_num = len(set(y_train))
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # word_2_index：所有word对应的数字
    # words_embedding：所有数字对应的向量
    word_2_index,words_embedding = build_curpus(X_train,embedding)

    train_dataset = TextDataset(X_train,y_train,word_2_index,max_len)
    # DataLoader用于多线程地读取数据，提取到一批数据后，就可以将其输入到网络中进行训练或推理
    # 需要使用自定义Dataset，并且至少应包含__init__、__len__和__getitem__这三个函数。其中，__init__用于传入数据，__len__返回数据集的大小（即item的数量），而__getitem__则用于返回一条训练数据，并将其转换为tensor
    train_loader = DataLoader(train_dataset,batch_size,shuffle=False)

    model = TextCNNModel(words_embedding,max_len,class_num).to(device)
    #
    opt = torch.optim.AdamW(model.parameters(),lr=lr)

    for e in range(epoch):
        for batch_idx,batch_label in train_loader:
            loss = model.forward(batch_idx,batch_label)
            loss.backward()
            opt.step()
            opt.zero_grad()
            print(f"loss:{loss:.3f}")

