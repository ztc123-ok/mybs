import argparse
import scrapy
from scrapy import Spider,Request
from ..items import CatchOneItem
from get_user_agent import get_user_agent_of_pc

class QunarSpider(scrapy.Spider):
    name = "catch_one"
    allowed_domains = ["travel.qunar.com"]
    start_urls = ['https://travel.qunar.com/']
    base_url = "https://travel.qunar.com/search/place/22-hangzhou-300195/4-----0/{}"
    #搜索url格式：https://travel.qunar.com/search/all/雷峰塔
    limit_page = 3

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
        url = self.base_url.format(1)
        yield Request(url=url,callback=self.parse)  # 依次抓取10页

    def parse(self, response):
        print("catch_one运行到parse",get_user_agent_of_pc())
        items = CatchOneItem()
        items['para_name'] = self.para_name
        yield items
