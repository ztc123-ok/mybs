import re
import emoji
import erniebot
from get_user_agent import get_user_agent_of_pc
import requests
from lxml import etree
import pymysql
import time
import random
import pandas as pd

erniebot.api_type = 'aistudio'
erniebot.access_token = '44d8a3f453895f463a6eba170db298dfbcb6466f'
data = pd.read_csv("./comment.csv", usecols=['content', 'rating'])
data = data.values # 评论文本数据 类别数据（好评/差评）

right_num = 0

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

i = 379
# while True:
#     if("这是一个快乐而轻松的行程。地接社导游很好，一路也很辛苦的全程陪同。谢谢阿峰给我们旅程中带来的快乐。这个行程里面" in data[i][0]):
#         break
#     i = i + 1
flag = 0
while i < len(data):
    print("第i: ", i)
    comment = data[i]
    time.sleep(1 + random.random())
    comment[0] = clean(comment[0])
    print("评论：\n",comment[0])
    response = erniebot.ChatCompletion.create(

    model='ernie-3.5',
    messages=[{
        "task_prompt": "SentimentClassification",
        'role': 'user',
        'content': "判断是好评还是差评？你只能回答好评或差评，不允许回答含有中性\n\"{}\"".format(comment[0])
    }])

    print(response.get_result())
    if '差评' in response.get_result() and '好评' not in response.get_result():
        if comment[1] == '差评':
            right_num = right_num + 1
            print("这个差评判断正确",right_num)
    elif '好评' in response.get_result() and '差评' not in response.get_result():
        if comment[1] == '好评':
            right_num = right_num + 1
            print("这个好评判断正确",right_num)
    else:
        flag  = flag + 1
        if flag == 3:
            flag = 0
        else:
            i = i - 1
    i = i + 1
# 0.92
print(f"acc = {right_num / len(comment) * 100:.2f}%")

