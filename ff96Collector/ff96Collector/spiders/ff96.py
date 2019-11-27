# -*- coding: utf-8 -*-
import scrapy


class Ff96Spider(scrapy.Spider):
    name = 'ff96'
    allowed_domains = ['96ff.net']
    start_urls = ['https://96ff.net/luyilu/']

    def parse(self, response):
        pass
