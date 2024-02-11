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

def get_url(sight_name):
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

    # 拼接携程搜索网址
    xc_url = "https://you.ctrip.com/sight/Hangzhou14.html?keywords={}".format(sight_name)
    chrome.get(xc_url)
    time.sleep(3 + random.random())
    html = chrome.page_source
    html_tree = etree.HTML(html)

    # 解析出网页第一个景点网址
    sight_url = html_tree.xpath("//*[@id='content']/div[4]/div/div[2]/div/div[3]/div/div[2]/dl/dt/a[1]/@href")
    sight_url = sight_url[0]
    if sight_name == '杭州海底世界':
        sight_url = 'https://you.ctrip.com/sight/hangzhou14/2476481.html'

    chrome.quit()

    return sight_url

def update_sight(url):
    print("正在更新景点。。。",url)
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

    # 景点评分   4.7 （注：满分5）|| 暂无评分
    comment_score = html_tree.xpath("//*[@class='comment']/div/p[1]/text()")
    # 景点评论数  16407
    comment_count = html_tree.xpath("//*[@class='comment']/p/span/text()[1]")
    # 景点热度   8.9 （注：满分10）
    heat_score = html_tree.xpath("//*[@class='titleView']/div[2]/div[1]/div/text()")
    # 景点开放状态（开园中/暂停营业）
    open_state = html_tree.xpath("//*[@class='baseInfoContent']/div[2]/p[2]/span[1]/text()")
    # 景点开放时间 06:30-17:30开放
    open_time = html_tree.xpath("//*[@class='baseInfoContent']/div[2]/p[2]/text()[2]")

    comment_score = ''.join(comment_score)
    comment_count = ''.join(comment_count)
    heat_score = ''.join(heat_score)
    open_state = ''.join(open_state)
    open_time = ''.join(open_time)

    connect = pymysql.Connect(host="localhost", user="root", password="root", port=3307, db="hangzhou",charset="utf8")
    cursor = connect.cursor()

    sql = "select id from xc_sight where url = '{}'".format(url)
    cursor.execute(sql)

    rest = cursor.fetchall()
    print("count", rest)
    if(len(rest)==0):
        with open("erro.txt", "a", encoding='utf-8') as f:
            f.writelines("数据库中没有该景点，无法更新，请先添加\n")
        chrome.quit()
        cursor.close()
        connect.close()
        return
    id = rest[0][0]
    # 更新景点信息
    sql = "UPDATE xc_sight SET comment_score={},comment_count={},heat_score={},open_state='{}',open_time='{}',update_time='{}' where id={}"\
        .format(comment_score,comment_count,heat_score,open_state,open_time,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),id)
    cursor.execute(sql)
    connect.commit()

    # 查询评论记录最新的日期
    sql = "SELECT comments_time FROM xc_comments_timesort WHERE sight_id={}".format(id)
    cursor.execute(sql)
    rest = cursor.fetchall()
    if (len(rest) == 0):
        latest_date = datetime.date(2023, 1, 1)
    else:
        latest_date = max(rest)[0]

    # 切换到时间排序
    try:
        time.sleep(1 + random.random())
        time_buttun = chrome.find_element(by=By.XPATH,
                                          value="//*[@class='commentModuleRef']/div/div[@class='sortList']/span[@class='sortTag']")
        # time_buttun.click()
        chrome.execute_script("arguments[0].click();", time_buttun)
    except:
        print("这个景点可能没有评价")

    page2 = 1
    print('时间排序page2:', page2)
    time.sleep(3 + random.random())
    html = chrome.page_source
    html_tree = etree.HTML(html)

    # 用户昵称
    comments_user_timesort = html_tree.xpath(
        "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[1]/div[2]/text()")
    # 评论
    comments_timesort = html_tree.xpath(
        "//*[@class='commentModuleRef']/div/div[@class='commentList']/div/div[2]/div[2]/text()")
    # 评论时间  2024-02-01
    comments_time_timesort = html_tree.xpath(
        "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[2]/div[@class='commentFooter']/div[1]/text()")
    # IP属地  浙江
    comments_ip_timesort = html_tree.xpath(
        "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[2]/div[@class='commentFooter']/div[1]/span/text()[2]")
    # 评论图片  url * n
    comments_pic_timesort = []
    for n in range(len(comments_timesort)):
        pic = html_tree.xpath(
            "//*[@class='commentModuleRef']//div[@class='commentList']/div[{}]/div[2]/div[@class='commentImgList']/a/@href".format(
                n + 1))
        comments_pic_timesort.append(','.join(pic))

    try:
        next_button = chrome.find_element(by=By.XPATH,
                                          value="//div[@class='myPagination']/ul/li[@title='下一页']")
        flag = next_button.get_attribute("aria-disabled")
    except:
        print("评论小于1页")
    print("上次更新时间：",latest_date)
    # 检查时间
    for i in range(len(comments_time_timesort)):
        date_object = parse(comments_time_timesort[i]).date()
        if date_object <= latest_date:
            comments_user_timesort = comments_user_timesort[:i]
            comments_timesort = comments_timesort[:i]
            comments_time_timesort = comments_time_timesort[:i]
            comments_ip_timesort = comments_ip_timesort[:i]
            comments_pic_timesort = comments_pic_timesort[:i]
            flag = 'true'
            break

        # true(没有下一页) false(有下一页)
    while (flag == 'false' and page2 < 301):
        next_page_buttun = chrome.find_element(by=By.XPATH,
                                               value="//div[@class='myPagination']/ul/li[@title='下一页']/span/a")
        chrome.execute_script("arguments[0].click();", next_page_buttun)
        # next_page_buttun.click()
        # WebDriverWait(chrome, timeout=10).until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, "//div[@class='myPagination']/ul/li[@title='下一页']/span/a"))).click()
        time.sleep(2 + random.random())
        page2 = page2 + 1
        if page2 % 10 == 0:
            time.sleep(1 + random.random())
        print('时间排序page2:', page2)
        html = chrome.page_source
        html_tree = etree.HTML(html)

        # 下一页用户昵称
        next_comments_user_timesort = html_tree.xpath(
            "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[1]/div[2]/text()")
        # 下一页评论
        next_comments_timesort = html_tree.xpath(
            "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[2]/div[2]/text()")
        # 下一页评论时间
        next_comments_time_timesort = html_tree.xpath(
            "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[2]/div[@class='commentFooter']/div[1]/text()")
        # 下一页评论ip
        next_comments_ip_timesort = html_tree.xpath(
            "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[2]/div[@class='commentFooter']/div[1]/span/text()[2]")
        # 下一页评论图片
        next_comments_pic_timesort = []
        for n in range(len(next_comments_timesort)):
            pic = html_tree.xpath(
                "//*[@class='commentModuleRef']//div[@class='commentList']/div[{}]/div[2]/div[@class='commentImgList']/a/@href".format(
                    n + 1))
            next_comments_pic_timesort.append(','.join(pic))

        # 检查下一页按钮状态
        next_button = chrome.find_element(by=By.XPATH,
                                          value="//div[@class='myPagination']/ul/li[@title='下一页']")
        flag = next_button.get_attribute("aria-disabled")

        # 检查时间
        for i in range(len(next_comments_time_timesort)):
            date_object = parse(next_comments_time_timesort[i]).date()
            if date_object <= latest_date:
                next_comments_user_timesort = next_comments_user_timesort[:i]
                next_comments_timesort = next_comments_timesort[:i]
                next_comments_time_timesort = next_comments_time_timesort[:i]
                next_comments_ip_timesort = next_comments_ip_timesort[:i]
                next_comments_pic_timesort = next_comments_pic_timesort[:i]
                flag = 'true'
                break
        # 合并
        comments_user_timesort = comments_user_timesort + next_comments_user_timesort
        comments_timesort = comments_timesort + next_comments_timesort
        comments_time_timesort = comments_time_timesort + next_comments_time_timesort
        comments_ip_timesort = comments_ip_timesort + next_comments_ip_timesort
        comments_pic_timesort = comments_pic_timesort + next_comments_pic_timesort

    # 清洗评论数据
    comments_user_timesort = clean(comments_user_timesort)
    comments_timesort = clean(comments_timesort)

    min_len = min(len(comments_user_timesort), len(comments_timesort),
                  len(comments_pic_timesort), len(comments_time_timesort))
    if (len(comments_user_timesort) != min_len or len(comments_timesort) != min_len or len(
            comments_ip_timesort) != min_len or len(comments_pic_timesort) != min_len or len(
            comments_time_timesort) != min_len):
        with open("erro.txt", "a", encoding='utf-8') as f:
            f.writelines(
                f"{len(comments_user_timesort)}, {len(comments_timesort)}, {len(comments_ip_timesort)}, {len(comments_pic_timesort)}, {len(comments_time_timesort)}," + str(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "\n")
    # 插入时间排序评论
    for i in range(min_len):

        if (min_len > 0):
            if (i >= len(comments_ip_timesort)):
                ip = '未知'
            else:
                ip = comments_ip_timesort[i]
            sql = "INSERT INTO xc_comments_timesort (sight_id,comments_user,comments,comments_ip,comments_pic,comments_time,create_time) VALUES ({},'{}','{}','{}','{}','{}','{}')".format(
                id, comments_user_timesort[i], comments_timesort[i], ip,
                comments_pic_timesort[i], comments_time_timesort[i],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            try:
                print("正在插入时间排序评论数据。。。")
                cursor.execute(sql)
                connect.commit()
            except BaseException as e:
                print('插入时间排序的评论有误', e)
                mystr = str(id) + "," + comments_user_timesort[i] + "," + comments_timesort[i] + "," + \
                        ip + "," + comments_pic_timesort[i] + "," + comments_time_timesort[
                            i] + "," + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                with open("erro.txt", "a", encoding='utf-8') as f:
                    f.writelines(mystr + "\n" + str(e) + "\n")
    print("景点已更新")
    chrome.quit()
    cursor.close()
    connect.close()

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