import scrapy
from ..items import SightsItem
from scrapy import Spider,Request
from lxml import etree
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from get_user_agent import get_user_agent_of_pc
import random

class CatchSightsSpider(scrapy.Spider):
    name = "catch_sights"
    allowed_domains = ["you.ctrip.com"]
    start_urls = ['https://you.ctrip.com/']
    base_url = "https://you.ctrip.com/sight/hangzhou14/s0-p{}.html#sightname"

    def start_requests(self):
        for i in range(1,3):
            url = self.base_url.format(i)
            with open("record.txt", "a") as f:
                f.writelines(str(i)+"\n")
            yield Request(url=url,callback=self.parse)  # 依次抓取10页

    def parse(self, response):
        html = response.text
        html_tree = etree.HTML(html)
        #景区详情链接
        sight_url = html_tree.xpath("//*[@id='content']/div[4]/div/div[2]/div/div[3]/div/div[2]/dl/dt/a[1]/@href")
        for url in(sight_url[:1]):
            items = SightsItem()
            items['url'] = url
            yield scrapy.Request(url,callback=self.parse_detail,meta={'items': items})

    def parse_detail(self, response):
        chrome_driver = "C:/Users/周/Desktop/selenium_example/chromedriver-win64/chromedriver-win64/chromedriver.exe"
        options = webdriver.ChromeOptions()
        # 隐藏窗口
        options.add_argument("--headless")
        options.add_argument("disable-infobars")
        options.add_argument("user-agent=" + get_user_agent_of_pc())
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome = webdriver.Chrome(options=options, executable_path=chrome_driver)
        chrome.maximize_window()
        # https://you.ctrip.com/sight/beijing1/s0-p2.html#sightname
        # https://you.ctrip.com/sight/hangzhou14/s0-p2.html#sightname
        # https://you.ctrip.com/sight/Hangzhou14/s0-p1000.html#sightname

        items = response.meta['items']
        page1 = 1 #智能排序
        page2 = 1 #时间排序
        html = response.text
        html_tree = etree.HTML(html)

        #景点名    灵隐寺
        name = html_tree.xpath("//*[@class='titleView']/div[1]/h1/text()")
        #景点评分   4.7 （注：满分5）
        comment_score = html_tree.xpath("//*[@class='comment']/div/p[1]/text()")
        #景点评论数  16407
        comment_count = html_tree.xpath("//*[@class='comment']/p/span/text()[1]")
        #景点热度   8.9 （注：满分10）
        heat_score = html_tree.xpath("//*[@class='titleView']/div[2]/div[1]/div/text()")
        #景点地址   杭州市西湖区灵隐路法云弄1号
        address = html_tree.xpath("//*[@class='baseInfoContent']/div[1]/p[2]/text()")
        #景点开放状态（开园中/暂停营业）
        open_state = html_tree.xpath("//*[@class='baseInfoContent']/div[2]/p[2]/span/text()")
        #景点开放时间 06:30-17:30开放
        open_time = html_tree.xpath("//*[@class='baseInfoContent']/div[2]/p[2]/text()[2]")
        #官方电话   0571-87968665
        phone = html_tree.xpath("//*[@class='baseInfoContent']/div[3]/p[2]/text()")
        #图片     （url * n）
        photos = html_tree.xpath("//*[@class='swiper']/div/div[1]/div/@style")
        for i in range(len(photos)):
            photos[i] = re.findall(r"[(](.*?)[)]", photos[i])[0]
        #景点介绍     p标签下需要拼接
        introduction = ''.join(html_tree.xpath("//*[@class='detailModuleRef']//div[@class='LimitHeightText']/div/p/text()"))
        #优待政策     div标签下需要拼接
        discount = ''.join(html_tree.xpath("//*[@class='detailModuleRef']/div/div[contains(text(), '优待政策')]/following-sibling::div[1]/div/text()"))
        #用户昵称
        comments_user = html_tree.xpath("//*[@class='commentModuleRef']//div[@class='commentList']/div/div[1]/div[2]/text()")
        #评论
        comments = html_tree.xpath("//*[@class='commentModuleRef']//div[@class='commentList']/div/div[2]/div[2]/text()")

        items['name'] = name
        items['comment_score'] = comment_score
        items['comment_count'] = comment_count
        items['heat_score'] = heat_score
        items['address'] = address
        items['open_state'] = open_state
        items['open_time'] = open_time
        items['phone'] = phone
        items['photos'] = photos
        items['introduction'] = introduction
        items['discount'] = discount

        chrome.get(items['url'])
        time.sleep(3 + random.random())
        flag = 'true'
        try:
            next_button = chrome.find_element(by=By.XPATH,
                                               value="//div[@class='myPagination']//li[@title='下一页']")
            flag = next_button.get_attribute("aria-disabled")
        except:
            print("评论小于1页")

        print('智能排序page:', page1)
        # true(没有下一页) false(有下一页)
        while (flag == 'false' and page1 < 2):
            next_page_buttun = chrome.find_element(by=By.XPATH,
                                               value="//div[@class='myPagination']//li[@title='下一页']/span/a")
            next_page_buttun.click()
            time.sleep(3 + random.random())

            page1 = page1+1
            print('page:', page1)
            html = chrome.page_source
            html_tree = etree.HTML(html)
            # 下一页用户昵称
            next_page_comments_user = html_tree.xpath(
                "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[1]/div[2]/text()")
            # 下一页评论
            next_page_comments = html_tree.xpath(
                "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[2]/div[2]/text()")
            comments_user = comments_user + next_page_comments_user
            comments = comments + next_page_comments
            next_button = chrome.find_element(by=By.XPATH,
                                                   value="//div[@class='myPagination']//li[@title='下一页']")
            flag = next_button.get_attribute("aria-disabled")

        #切换到时间排序
        try:
            time_buttun = chrome.find_element(by=By.XPATH,
                                                    value="//*[@class='commentModuleRef']//div[@class='sortList']/span[2]")
            time_buttun.click()
            time.sleep(3 + random.random())
        except:
            print("这个景点可能没有评价")

        print('时间排序page:', page2)

        # 用户昵称
        comments_user_timesort = html_tree.xpath(
            "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[1]/div[2]/text()")
        # 评论
        comments_timesort = html_tree.xpath("//*[@class='commentModuleRef']//div[@class='commentList']/div/div[2]/div[2]/text()")

        try:
            next_button = chrome.find_element(by=By.XPATH,
                                               value="//div[@class='myPagination']//li[@title='下一页']")
            flag = next_button.get_attribute("aria-disabled")
        except:
            print("评论小于1页")

        # true(没有下一页) false(有下一页)
        while (flag == 'false' and page2 < 2):
            next_page_buttun = chrome.find_element(by=By.XPATH,
                                                        value="//div[@class='myPagination']//li[@title='下一页']/span/a")
            next_page_buttun.click()
            time.sleep(3 + random.random())

            page2 = page2 + 1
            print('page:', page2)
            html = chrome.page_source
            html_tree = etree.HTML(html)
            # 下一页用户昵称
            next_page_comments_user_timesort = html_tree.xpath(
                "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[1]/div[2]/text()")
            # 下一页评论
            next_page_comments_timesort = html_tree.xpath(
                "//*[@class='commentModuleRef']//div[@class='commentList']/div/div[2]/div[2]/text()")
            comments_user_timesort = comments_user + next_page_comments_user_timesort
            comments_timesort = comments + next_page_comments_timesort
            next_button = chrome.find_element(by=By.XPATH,
                                                   value="//div[@class='myPagination']//li[@title='下一页']")
            flag = next_button.get_attribute("aria-disabled")

        items['comments_user'] = comments_user
        items['comments'] = comments
        items['comments_user_timesort'] = comments_user_timesort
        items['comments_timesort'] = comments_timesort

        chrome.quit()

        yield items

