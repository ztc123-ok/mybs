import re
import emoji
import erniebot
from get_user_agent import get_user_agent_of_pc
import requests
from lxml import etree
import pymysql
erniebot.api_type = 'aistudio'
erniebot.access_token = 'c2610a49f190eb3839deea2b1bef8ea5ea1fa39e'

response = erniebot.ChatCompletion.create(
    model='ernie-3.5',
    messages=[{
        'role': 'user',
        'content': "请问你是谁？"
    }, {
        'role': 'assistant',
        'content':
        "我是百度公司开发的人工智能语言模型，我的中文名是文心一言，英文名是ERNIE-Bot，可以协助您完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果您有任何问题，请随时向我提问。"
    }, {
        'role': 'user',
        'content': "我在深圳，周末可以去哪里玩？"
    }])

print(response.get_result())