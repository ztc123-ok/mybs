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
# print(len("4008888518,0571-82880333,0571-82880222"))

def clean(list, restr=''):
    # 过滤表情,我还得专门下个emoji的库可还行，数据库字段设utf8mb4好像也行,字段里含有‘和“写sql也会错
    # 谁家取昵称还带表情啊
    try:
        co = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55]+')
    except re.error:
        co = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u2B55])+')
    if (isinstance(list, str)):
        list = co.sub(restr, list)
        list = emoji.replace_emoji(list, restr)
        list = list.replace("'", restr).replace('"', restr)
    else:
        for i in range(len(list)):
            list[i] = co.sub(restr, list[i])
            list[i] = emoji.replace_emoji(list[i], restr)
            list[i] = list[i].replace("'", restr).replace('"', restr)

    return list

mystr = "这次坐车是家人公认在杭州最开心的一次了，天气凉爽坐在上层，钱塘江两岸很美，就是木头座位'坐着不舒服。,未知,,2018-09-10,2024-02-04 17:35:36"
print(clean(mystr))
