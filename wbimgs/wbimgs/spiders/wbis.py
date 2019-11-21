# -*- coding: utf-8 -*-
import scrapy
from wbimgs.items import WbimgsItem
import re


class WbisSpider(scrapy.Spider):
    name = 'wbis'
    allowed_domains = ['m.weibo.cn']
    start_urls = [
        # whYUEspecial·杨超越
        # 'https://m.weibo.cn/u/2676540645?uid=2676540645&luicode=10000011&lfid=1008082a98366b6a3546bd16e9da0571e34b84_-_soul',
        # ChampagneRose_杨超越个站
        # 'https://m.weibo.cn/u/5951606667?uid=5951606667&luicode=10000011&lfid=1076035951606667',
        # 杨超越的摸鱼基地
        'https://m.weibo.cn/u/7165916155?uid=7165916155&luicode=10000011&lfid=1076037165916155'
    ]

    def parse(self, response):
        # 解析网页，并提取需要的数据。response为url请求返回的结果即需要进行解析的网页
        # img元素的xpath '//article//div[@class="weibo-og"]//li[@class="m-auto-box"]//img'
        # img元素中src属性的xpath '//article//div[@class="weibo-og"]//li[@class="m-auto-box"]//img/attribute::src'
        # 从选择权Selector中提取data,需要调用extract()方法

        # 方式1：仅采用imgrul中的图片名称作为名字，确定图片名称排列无序, imgpath设置无效，pipelines自动实现命名
        src_urls = response.xpath('//article//div[@class="weibo-og"]//li[@class="m-auto-box"]//img/attribute::src').extract()
        for src_url in src_urls:
            item = WbimgsItem()
            item['imglink'] = re.sub("orj360", 'large', src_url)
            item['imgpath'] = '666' + src_url.split('/')[-1]
            yield item

        # 方式2：截去微博文本中的一部分作为名称前缀, 此方式未摸透，暂不采用
        # weibo_ogs = response.xpath('//article//div[@class="weibo-og"]')
        # for weibo in weibo_ogs:
        #     # print(weibo)
        #     weibo_texts = weibo.xpath('//div[@class="weibo-text"]/text()').extract()
        #     # print('weibo_texts', weibo_texts)
        #     src_urls = weibo.xpath('//li[@class="m-auto-box"]//img/attribute::src').extract()
        #     imgtag = ''.join(weibo_texts)
        #     new_imgtag = ''.join(re.compile(r'[0-9]+|[\u4e00-\u9fa5]+|[a-z]', re.I).findall(imgtag))
        #     id = 0
        #     for src_url in src_urls:
        #         id += 1
        #         item = WbimgsItem()
        #         item['imglink'] = re.sub("orj360", 'large', src_url)
        #         item['imgpath'] = new_imgtag[:20] + str(id) + '.jpg'
        #         yield item

