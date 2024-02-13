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
erniebot.access_token = ''
data = pd.read_csv("./comment.csv", usecols=['content', 'rating'])
data = data.values # 评论文本数据 类别数据（好评/差评）

right_num = 0

for comment in data:
    time.sleep(1 + random.random())
    response = erniebot.ChatCompletion.create(

    model='ernie-3.5',
    messages=[{
        "task_prompt": "SentimentClassification",
        'role': 'user',
        'content': "判断是好评还是差评？0代表差评，1代表好评,你只能回答0或1\n\"{}\"".format(comment[0])
    }])

    print(response.get_result())
    if comment[1] == '差评' and '0' in response.get_result():
        right_num = right_num + 1
        print(right_num)
    if comment[1] == '好评' and '1' in response.get_result():
        right_num = right_num + 1
        print(right_num)
print(f"acc = {right_num / len(comment) * 100:.2f}%")

