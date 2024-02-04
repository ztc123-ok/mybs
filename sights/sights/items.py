# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SightsItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    comment_score = scrapy.Field()
    comment_count = scrapy.Field()
    heat_score = scrapy.Field()
    address = scrapy.Field()
    open_state = scrapy.Field()
    open_time = scrapy.Field()
    phone = scrapy.Field()
    photos = scrapy.Field()
    introduction = scrapy.Field()
    discount = scrapy.Field()
    comments_user = scrapy.Field()
    comments = scrapy.Field()
    comments_time = scrapy.Field()
    comments_ip = scrapy.Field()
    comments_pic = scrapy.Field()
    comments_user_timesort = scrapy.Field()
    comments_timesort = scrapy.Field()
    comments_time_timesort = scrapy.Field()
    comments_ip_timesort = scrapy.Field()
    comments_pic_timesort = scrapy.Field()