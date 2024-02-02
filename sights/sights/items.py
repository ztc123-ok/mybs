# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SightsItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    name = scrapy.Field()
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
    comments_user_timesort = scrapy.Field()
    comments_timesort = scrapy.Field()