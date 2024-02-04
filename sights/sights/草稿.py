import re
import emoji
import erniebot
from get_user_agent import get_user_agent_of_pc
import requests
from lxml import etree
import pymysql
# erniebot.api_type = 'aistudio'
# erniebot.access_token = 'c2610a49f190eb3839deea2b1bef8ea5ea1fa39e'
#
# response = erniebot.ChatCompletion.create(
#     model='ernie-3.5',
#     messages=[{
#         'role': 'user',
#         'content': "请问你是谁？"
#     }, {
#         'role': 'assistant',
#         'content':
#         "我是百度公司开发的人工智能语言模型，我的中文名是文心一言，英文名是ERNIE-Bot，可以协助您完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果您有任何问题，请随时向我提问。"
#     }, {
#         'role': 'user',
#         'content': "我在深圳，周末可以去哪里玩？"
#     }])
#
# print(response.get_result())

# connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
#                           charset="utf8")
# cursor = connect.cursor()
# sql = "select id from xc_sight where url = '{}'".format("https://you.ctrip.om/sight/hangzhou14/135838.html")
# cursor.execute(sql)
#
# rest = cursor.fetchall()
# print("count", len(rest))
print(len("https://dimg04.c-ctrip.com/images/1mh2312000c7al8vxC7DF_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh5z12000c7al1wdB731_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh0412000c7ah34c902B_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh4o12000c7achmy504C_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh3312000c7anwr7D9ED_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh1312000c7aen2s7CE6_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh6g12000c7aief7D2B9_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh3u12000c7agcys1BF4_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh1812000c7abt1z0595_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh2p12000c7acmy56C6C_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh0y12000c7adk40612B_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh2i12000c7ad6xs4ED1_W_640_10000.jpg?proc=autoorient,https://dimg04.c-ctrip.com/images/1mh1b12000c7aev9f0FD6_W_640_10000.jpg?proc=autoorient"))

# def clean(list, restr=''):
#     # 过滤表情,我还得专门下个emoji的库可还行，数据库字段设utf8mb4好像也行,字段里含有‘和“写sql也会错
#     # 谁家取昵称还带表情啊
#     try:
#         co = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55]+')
#     except re.error:
#         co = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+')
#     if (isinstance(list, str)):
#         list = co.sub(restr, list)
#         list = emoji.replace_emoji(list, restr)
#         list = list.replace("'", restr).replace('"', restr)
#     else:
#         for i in range(len(list)):
#             list[i] = co.sub(restr, list[i])
#             list[i] = emoji.replace_emoji(list[i], restr)
#             list[i] = list[i].replace("'", restr).replace('"', restr)
#
#     return list
#
# mystr = "这次坐车是家人公认在杭州最开心的一次了，天气凉爽坐在上层，钱塘江两岸很美，就是木头座位'坐着不舒服。,未知,,2018-09-10,2024-02-04 17:35:36"
# print(clean(mystr))
