# -*- coding: utf-8 -*-
import scrapy
import re
from ff96Collector.items import Ff96CollectorItem




class Ff96Spider(scrapy.Spider):
    name = 'ff96'
    allowed_domains = ['96ff.net']
    start_urls = [
        'https://96ff.net/luyilu/list_5_{}.html'.format(i) for i in range(1, 2)
    ]

    def parse(self, response):
        print('正在该页面解析文件地址， {}'.format(response.url))



