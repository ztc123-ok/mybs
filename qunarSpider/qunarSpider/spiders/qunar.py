import argparse
import scrapy
from scrapy import Spider,Request
from ..items import QunarspiderItem
from lxml import etree
import re
import time
import emoji
import random

class QunarSpider(scrapy.Spider):
    name = "qunar"
    allowed_domains = ["travel.qunar.com"]
    start_urls = ['https://travel.qunar.com/']
    # 共1-135页景点
    base_url = "https://travel.qunar.com/search/place/22-hangzhou-300195/4-----0/{}"
    #搜索url格式：https://travel.qunar.com/search/all/雷峰塔
    limit_page = 3 #限制评论页数
    start_page = 1 #爬取起始页
    end_page = 2 #爬取结束页

    para_name = "没接收到para_name"
    val = "没接收到val"

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--para_name', type=str, default=None)
        parser.add_argument('--age', default=None)
        args = parser.parse_args()
        para_name = args.para_name
        val = args.age
        if para_name == None:
            # with open("erro.txt", "a", encoding='utf-8') as f:
            #     f.writelines("erro" + "\n")
            print("name未传递使用默认参数,传参请使用--para_name")
        else:
            self.para_name = para_name
        if val == None:
            print("val未传递使用默认参数,传参请使用--para_age")
        else:
            self.val = val
        print('init中接收到para_name: ', para_name)
        print('init中接收到val: ', val)

    def start_requests(self):
        #共1-135页景点
        for i in range(self.start_page,self.end_page):
            time.sleep(2 + random.random())
            url = self.base_url.format(i)
            with open("record.txt", "a") as f:
                f.writelines(str(i)+"\n")
            yield Request(url=url,callback=self.parse)  # 依次抓取10页

    def parse(self, response):

        html = response.text
        html_tree = etree.HTML(html)
        # 景点详情链接
        sight_url = html_tree.xpath("//div[@class='right_bar']/ul/li/div[2]/h2/a/@href")
        print("urls",sight_url)
        for url in sight_url[:2]:
            time.sleep(2 + random.random())
            items = QunarspiderItem()
            items['para_name'] = self.para_name
            items['url'] = url
            #yield scrapy.Request(url,callback=self.parse_detail,meta={'items': items})
            yield Request(url=url,callback=self.parse_detail,meta={'items':items})

    def parse_detail(self, response):
        items = response.meta['items']

        html = response.text
        print(html)
        html_tree = etree.HTML(html)

        #景点名称    灵隐寺
        name = html_tree.xpath("//*[@class='main_leftbox']/div/h1[@class='tit']/text()")
        #景点评分   4.7 （注：满分5）
        comment_score = html_tree.xpath("//*[@class='main_leftbox']/div[@class='b_focus']//span[@class='cur_score']/text()")
        #门票  免费 || 40 || null
        ticket = html_tree.xpath("//*[@class='b_detail_info']/div/div[@id='mp']/div[2]/p/text()")
        #旅游时节   四季皆宜。
        travel_time = html_tree.xpath("//*[@class='b_detail_info']/div/div[@id='lysj']/div[2]/p/text()")
        #交通指南   ;;地铁;;地铁1号线到龙翔桥站，出站步行400米步行就到西湖。'
        transportation_p = html_tree.xpath("//*[@class='b_detail_info']/div/div[@id='jtzn']/div[2]/p")
        transportation = ''
        for element in transportation_p:
            try:
                if (element.find('b') != None):
                    transportation = transportation + ";;" + element.find('b').text + ";;"
                elif (element.find('strong') != None):
                    transportation = transportation + ";;" + element.find('strong').text + ";;"
                else:
                        transportation = transportation + element.text
            except:
                pass
        #建议游览时间    2小时
        tip_time = html_tree.xpath("//*[@class='main_leftbox']/div[@class='b_focus']//div[@class='txtbox']/div[@class='time']/text()")

        items['name'] = self.clean(''.join(name))
        items['comment_score'] = ''.join(comment_score)
        items['ticket'] = self.clean(''.join(ticket))
        items['travel_time'] = ''.join(travel_time)
        items['transportation'] = self.clean(''.join(transportation))
        items['tip_time'] = self.clean(''.join(tip_time))

        yield items

    def clean(self,list,restr=''):
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



