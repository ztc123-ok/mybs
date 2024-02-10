# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QunarspiderItem(scrapy.Item):
    para_name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    comment_score = scrapy.Field()
    ticket = scrapy.Field()
    travel_time = scrapy.Field()
    transportation = scrapy.Field()
    tip_time = scrapy.Field()

class CatchOneItem(scrapy.Item):
    para_name = scrapy.Field()
