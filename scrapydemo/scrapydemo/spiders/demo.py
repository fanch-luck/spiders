# -*- coding: utf-8 -*-
import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['www.demo.com']
    start_urls = ['http://www.demo.com/']

    def parse(self, response):
        pass
