import requests
import json
from get_user_agent import get_user_agent_of_pc
from lxml import etree
from selenium import webdriver
import time
import random
import pymysql

def get_passenger(url):
    chrome_driver = "D:/桌面/selenium_example/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    options = webdriver.ChromeOptions()
    # 隐藏窗口
    options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument("user-agent=" + get_user_agent_of_pc())
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome = webdriver.Chrome(options=options, executable_path=chrome_driver)
    chrome.maximize_window()
    # https://you.ctrip.com/sight/beijing1/s0-p2.html#sightname

    chrome.get(url)
    time.sleep(3 + random.random())
    html = chrome.page_source
    html_tree = etree.HTML(html)

    #景点名称    灵隐寺
    sight_name = html_tree.xpath("//*[@class='tab']/table/tbody/tr/td[2]/text()")
    #客流指数    84.71
    passenger_index = html_tree.xpath("//*[@class='tab']/table/tbody/tr/td[3]/text()")
    #拥堵指数    1.171
    traffic_index = html_tree.xpath("//*[@class='tab']/table/tbody/tr/td[5]/text()")
    #拥堵类型    畅通
    traffic_type = html_tree.xpath("//*[@class='tab']/table/tbody/tr/td[5]/span/b/text()")
    #拥堵里程    0.33（公里）
    traffic_mileage = html_tree.xpath("//*[@class='tab']/table/tbody/tr/td[7]/text()")
    #平均时速    37.09（km/h）
    average_speed = html_tree.xpath("//*[@class='tab']/table/tbody/tr/td[8]/text()")
    # time.strftime("%Y-%m-%d", time.localtime())

    # print(sight_name)
    # print(passenger_index)
    # print(traffic_index)
    # print(traffic_type)
    # print(traffic_mileage)
    # print(average_speed)

    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",
                                           charset="utf8")
    cursor = connect.cursor()

    print("开始向数据库插入客流数据。。。。")
    for i in range(len(sight_name)):
        # 两个网站景点名不一样，去携程找一下名字
        xc_url = "https://you.ctrip.com/sight/Hangzhou14.html?keywords={}".format(sight_name[i])
        chrome.get(xc_url)
        time.sleep(2 + random.random())
        html = chrome.page_source
        html_tree = etree.HTML(html)
        sight_url = html_tree.xpath("//*[@id='content']/div[4]/div/div[2]/div/div[3]/div/div[2]/dl/dt/a[1]/@href")
        if sight_name[i] == '杭州海底世界':
            sight_url = 'https://you.ctrip.com/sight/hangzhou14/2476481.html'
        #查询景点id 和 热度
        sql = "SELECT id,heat_score FROM xc_sight where url='{}'".format(sight_url[0])
        cursor.execute(sql)
        rest = cursor.fetchall()
        if (len(rest) == 0):
            sight_id = 'null'
            heat_score = 'null'
        else:
            sight_id = rest[0][0]
            heat_score = rest[0][1]

        sql = "INSERT INTO passenger (sight_id,sight_name,passenger_index,traffic_index,traffic_type,traffic_mileage,average_speed,heat_score,mydate) VALUES ({},'{}',{},{},'{}',{},{},{},'{}')"\
            .format(
            sight_id,sight_name[i], passenger_index[i], traffic_index[i],traffic_type[i], traffic_mileage[i],average_speed[i],heat_score,time.strftime("%Y-%m-%d", time.localtime())
            )
        try:
            print("正在插入客流数据数据。。。")
            cursor.execute(sql)
            connect.commit()
        except BaseException as e:
            print('插入智能的评论有误', e)
            mystr = sight_name[i] + "," + passenger_index[i] + "," + \
                traffic_index[i] + "," + traffic_type[i] + "," + traffic_mileage[i] + "," +average_speed[i]+","+ str(time.strftime("%Y-%m-%d", time.localtime()))
            with open("erro.txt", "a", encoding='utf-8') as f:
                f.writelines(mystr + "\n" + str(e) + "\n")
    cursor.close()
    connect.close()
    chrome.quit()

# 车主指南
url = 'https://www.icauto.com.cn/gonglu/yd_3301001.html'
get_passenger(url)



