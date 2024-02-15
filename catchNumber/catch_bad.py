from get_user_agent import get_user_agent_of_pc
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pymysql
import datetime
import emoji
import re
import csv
from dateutil.parser import parse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_path = "D:/桌面/selenium_example/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# 创建一个chrome
def get_chrome(chrome_path):
    chrome_driver = chrome_path
    options = webdriver.ChromeOptions()
    # 隐藏窗口
    #options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument("user-agent=" + get_user_agent_of_pc())
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome = webdriver.Chrome(options=options, executable_path=chrome_driver)
    chrome.maximize_window()
    return chrome

def get_url(url,page,mytype):
    print("正在获取{}。。。".format(mytype),url)
    if mytype == "好评":
        type_id = "2"
        mypath = "good.csv"
    elif mytype == "差评":
        type_id = "4"
        mypath = "bad.csv"

    chrome = get_chrome(chrome_path)
    # https://you.ctrip.com/sight/beijing1/s0-p2.html#sightname

    chrome.get(url)
    time.sleep(5 + random.random())

    # 好评 2  差评 4
    bad_button = chrome.find_element(by=By.XPATH,
                                      value="//*[@id='dpType']/div[@typeid='{}']/i".format(type_id))
    bad_button.click()
    # WebDriverWait(chrome, timeout=10).until(
    #      EC.presence_of_element_located(
    #          (By.XPATH, "//*[@id='dpType']/div[@typeid='4']/i"))).click()
    print("已点击",mytype)
    time.sleep(3 + random.random())
    for i in range(page):
        print("page: ",i)
        html = chrome.page_source
        html_tree = etree.HTML(html)
        comments = html_tree.xpath(
            "//*[@id='dp-con']/div[@class='info_list mtop']//p[@class='dpdetail']/text() | //*[@id='dp-con']/div[@class='info_list mtop']//p[@class='dpdetail']/b/text()")
        #print(comments)

        with open(mypath, 'a', newline='',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # 遍历数据并写入
            for co in comments:
                co = clean(co)
                row = [co,mytype]
                #row = [co, "差评"]
                writer.writerow(row)
        try:
            next_button = chrome.find_element(by=By.XPATH,
                                             value="//*[@id='pageNum_title']/div[@class='pageNum_page']/div/a[@class='guidnum nextNormal']")
            next_button.click()
        except:
            break
        time.sleep(2 + random.random())
    chrome.quit()

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

def catch_url(url):
    chrome = get_chrome(chrome_path)
    chrome.get(url)
    time.sleep(3 + random.random())
    for i in range(100):
        print("page: ",i)
        html = chrome.page_source
        html_tree = etree.HTML(html)
        urls = html_tree.xpath(
            "//*[@id='sceneryListInfo']/div//div[@class='s_info']/a/@href")
        #print(comments)

        with open('bad_url.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # 遍历数据并写入
            for co in urls:
                co = "https:" + co
                row = [co]
                writer.writerow(row)
        try:
            next_button = chrome.find_element(by=By.XPATH,
                                             value="//*[@id='pageNum_title']/div/a[@class='next_page02 border_gray']")
            next_button.click()
        except:
            break
        time.sleep(2 + random.random())
    chrome.quit()

import argparse

if __name__ == "__main__":
    url = "https://so.ly.com/scenery?q=%E5%8C%97%E4%BA%AC&c=0&classify=0&grade="
    page = 20
    mytype = "差评"
    #catch_url(url)
    with open('bad_url.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            i = i + 1
            # if i <= 1:
            #     continue
            get_url(row[0],page,mytype)
    # get_url(url,page)