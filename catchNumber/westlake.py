#https://search.zj.gov.cn/jrobotfront/search.do?websiteid=330150000000000&searchid=&pg=&p=1&tpl=2306&cateid=370&fbjg=&word=2023景点客流量&temporaryQ=&synonyms=&checkError=1&isContains=1&q=2023景点客流量&jgq=&eq=&begin=&end=&timetype=&_cus_pq_ja_type=&pos=&sortType=2
# 从2018年开始
# 来源:杭州西湖风景名胜区管委会  - 统计数据
import requests
from lxml import etree
from get_user_agent import get_user_agent_of_pc
from get_user_agent import get_user_agent_of_pc
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pymysql
from datetime import datetime, date
import emoji
import re
from dateutil.parser import parse
from urllib.parse import unquote
from dateutil.relativedelta import relativedelta

chrome_path = "D:/桌面/selenium_example/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# 创建一个chrome
def get_chrome(chrome_path):
    chrome_driver = chrome_path
    options = webdriver.ChromeOptions()
    # 隐藏窗口
    options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument("user-agent=" + get_user_agent_of_pc())
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome = webdriver.Chrome(options=options, executable_path=chrome_driver)
    chrome.maximize_window()
    return chrome

# 获取景点网址
def get_month_url(year):
    chrome = get_chrome(chrome_path)

    page = 1
    month_url = {} # 收费景点各月的网址的字典

    while True:
        # 政府官网
        search_url = "https://search.zj.gov.cn/jrobotfront/search.do?websiteid=330150000000000&searchid=&pg=&p={}&tpl=2306&cateid=370&fbjg=&word={}%E6%99%AF%E7%82%B9%E5%AE%A2%E6%B5%81&temporaryQ=&synonyms=&checkError=1&isContains=1&q={}%E6%99%AF%E7%82%B9%E5%AE%A2%E6%B5%81&jgq=&eq=&begin=&end=&timetype=&_cus_pq_ja_type=&pos=&sortType=2".format(
            page, year, year)
        chrome.get(search_url)

        time.sleep(3 + random.random())
        html = chrome.page_source
        html_tree = etree.HTML(html)

        westlake_url = html_tree.xpath("//div[@class='searchContent']//div[@class='comprehensive']/div/div[1]/a/@href")
        print("page:",page,"页面网址:",len(westlake_url))

        if len(westlake_url) == 0:
            break
        for i in range(len(westlake_url)):
            westlake_url[i] = "https://search.zj.gov.cn/jrobotfront/" + westlake_url[i]
            encoded_string = westlake_url[i].split("title=")[1]
            decoded_string = unquote(encoded_string)
            print(decoded_string)
            if "月" in decoded_string:
                try:
                    month = int(decoded_string.split("月")[0].split("年")[1])
                    month_url[month] = westlake_url[i]
                except:
                    print("日期转换错误",westlake_url[i])
                    with open("erro.txt", "a", encoding='utf-8') as f:
                        f.writelines("日期转换错误"+"\n"+westlake_url[i]+"\n")

        page = page + 1

    print("month_url:",month_url)
    print("month_url长度",len(month_url))
    chrome.quit()
    # 收费景点各月的网址的字典 {12:url}
    return month_url

# 获取景点详细数据
def parse_detail(url):
    chrome = get_chrome(chrome_path)

    chrome.get(url)

    time.sleep(3 + random.random())
    html = chrome.page_source
    html_tree = etree.HTML(html)

    # 景点名 灵隐飞来峰
    sight_name = html_tree.xpath("//div[@id='zoom']//tr/td[1]/text() | //div[@id='zoom']//tr/td[1]/span[1]/text() | //div[@id='zoom']//tr/td[1]/p[1]/text() | //div[@id='zoom']//tr/td[1]/p[1]/span[1]/text()")[-8:]
    # 客流量 28.70（万）
    passenger_number = html_tree.xpath("//div[@id='zoom']//tr/td[3]/text() | //div[@id='zoom']//tr/td[3]/span[1]/text() | //div[@id='zoom']//tr/td[3]/p[1]/text() | //div[@id='zoom']//tr/td[3]/p[1]/span[1]/text()")[-8:]
    sight_name = [x.strip() for x in sight_name]
    passenger_number = [x.strip() for x in passenger_number]
    print(sight_name)
    print(passenger_number)

    chrome.quit()
    return sight_name,passenger_number

# 插入数据库
def insert_into(sight_name,passenger_number,mydate):
    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",charset="utf8")
    cursor = connect.cursor()

    sql = "SELECT DISTINCT sight_name, sight_id FROM westlake"
    cursor.execute(sql)
    rest = cursor.fetchall()
    id_dict = dict(rest)

    for i in range(len(sight_name)):
        if sight_name[i] in id_dict:
            sight_id = id_dict[sight_name[i]]
        else:
            sight_id = "null"

        sql = "INSERT INTO westlake(sight_id,sight_name,passenger_number,mydate) VALUES({},'{}',{},'{}')".format(sight_id,sight_name[i],passenger_number[i],mydate)
        try:
            print("正在插入西湖景点数据。。。")
            cursor.execute(sql)
            connect.commit()
        except BaseException as e:
            print('插入客流数据数据有误', e)
            mystr = sight_id + "," + sight_name[i] + "," + passenger_number[i] + "," + \
                    mydate + "," + str(time.strftime("%Y-%m-%d", time.localtime()))
            with open("erro.txt", "a", encoding='utf-8') as f:
                f.writelines(mystr + "\n" + str(e) + "\n")

    cursor.close()
    connect.close()

# 查询评论记录最新的日期
def get_latest_date():
    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",charset="utf8")
    cursor = connect.cursor()

    sql = "SELECT DISTINCT mydate FROM westlake"
    cursor.execute(sql)
    rest = cursor.fetchall()

    if (len(rest) == 0):
        # 获取当前时间
        now = datetime.now()
        # 提取年份和月份
        year = now.year
        month = now.month
        print("数据库中没有记录，生成当前时间")
        latest_date = date(year, month, 1)
    else:
        latest_date = max(rest)[0]
    cursor.close()
    connect.close()
    return latest_date

# 获取最新数据，依照政府官网一个月更新一次
def update():
    now = datetime.now()
    # 提取年份和月份
    year = now.year
    month = now.month
    now_date = date(year, month, 1)
    latest_date = get_latest_date()
    #latest_date = date(2017, 12, 1)
    temp_year = 9999
    month_url = {}
    while now_date > latest_date:
        latest_date = latest_date + relativedelta(months=1)
        if latest_date.year != temp_year:
            month_url = get_month_url(latest_date.year)
            temp_year = latest_date.year
        if len(month_url) == 0:
            continue
        print("正在获取。。。",latest_date)
        url = month_url[latest_date.month]
        sight_name,passenger_number = parse_detail(url)
        insert_into(sight_name,passenger_number,latest_date)
# 每个月更新一次
update()


