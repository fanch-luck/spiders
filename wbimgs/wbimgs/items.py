# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WbimgsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # title = scrapy.Field()  # 图片主题
    imglink = scrapy.Field()  # 图片真实下载地址
    imgpath = scrapy.Field()  # 图片保存路径
    pass
