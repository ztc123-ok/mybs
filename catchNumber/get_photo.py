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
from dateutil.parser import parse

chrome_path = "D:/桌面/selenium_example/chromedriver-win64/chromedriver-win64/chromedriver.exe"

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

def get_photo(url):
    print("正在获取图片。。。",url)
    chrome = get_chrome(chrome_path)
    # https://you.ctrip.com/sight/beijing1/s0-p2.html#sightname

    chrome.get(url)
    time.sleep(3 + random.random())
    html = chrome.page_source
    html_tree = etree.HTML(html)

    photo = ''.join(html_tree.xpath("//body/img/@src"))
    return photo

def get_url():
    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",charset="utf8")
    cursor = connect.cursor()

    sql = "select id,photos from xc_sight"
    cursor.execute(sql)
    rest = dict(cursor.fetchall())
    cursor.close()
    connect.close()
    return rest

def update_photo(id,photos):
    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",charset="utf8")
    cursor = connect.cursor()

    sql = "update xc_sight set photos = '{}' where id = {}".format(photos,id)
    cursor.execute(sql)
    connect.commit()
    cursor.close()
    connect.close()


if __name__ == "__main__":
    # url = "https://dimg04.c-ctrip.com/images/100v0h00000091vol6690_D_521_391.jpg"
    urls = get_url()
    for id, photos in urls.items():
        print("当前景点id",id)
        photos_url = photos.split(",")
        photo_list = []
        for photo in photos_url:
            photo = photo.split("\"")[1]
            photo_list.append(get_photo(photo))
        update_photo(id,",".join(photo_list))
