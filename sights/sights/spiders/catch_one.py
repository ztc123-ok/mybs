import scrapy
from ..items import SightsItem
from scrapy import Spider,Request
from lxml import etree
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from get_user_agent import get_user_agent_of_pc
import random
import emoji
import argparse

class CatchSightsSpider(scrapy.Spider):
    name = "catch_sights"
    allowed_domains = ["you.ctrip.com"]
    start_urls = ['https://you.ctrip.com']