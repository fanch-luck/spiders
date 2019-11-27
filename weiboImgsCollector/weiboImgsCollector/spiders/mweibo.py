# -*- coding: utf-8 -*-
import scrapy
from requests_html import HTML
from weiboImgsCollector.items import WeiboimgscollectorItem
import re


class MweiboSpider(scrapy.Spider):
    name = 'mweibo'
    allowed_domains = ['m.weibo.cn']
    start_urls = [
        # ChampagneRose_杨超越个站
        'https://m.weibo.cn/u/5951606667?uid=5951606667&luicode=10000011&lfid=1076035951606667'
    ]

    def parse(self, response):
        weibo_imgs = []
        # f = open('E:\MyWorkPlace\spiders\weiboImgsCollector\weiboImgsCollector\source.html', 'r', encoding='utf-8')
        # ff = f.read()
        # f.close()
        html = HTML(html=response.body.decode('utf-8'))
        # print(html.html)
        weibo_ogs = html.xpath('//article//div[@class="weibo-og"]')  # 微博原po内容卡片
        print('匹配数： ', len(weibo_ogs))
        for weibo_og in weibo_ogs:
            if weibo_og.xpath('//div/div[@class="weibo-media-wraps weibo-media media-b"]//img'):
                weibo_texts = weibo_og.xpath('//div/text()')  # 提取微博内容文本str
                #print(weibo_texts)
                text = ''.join([x for x in weibo_texts])
                title = ''.join(re.compile(r'[0-9]+|[\u4e00-\u9fa5]+|[a-z]', re.I).findall(text))
                src_urls = weibo_og.xpath('//div//img/attribute::src')  # 微博图片链接str
                for src_url in src_urls:
                    if src_url[-4:] == '.jpg':
                       img = dict()
                       img["title"] = title
                       img["link"] = src_url
                       weibo_imgs.append(img)
        for img in weibo_imgs:
            print('img: ', img)
            item = WeiboimgscollectorItem()
            item['imgtitle'] = img["title"]
            item['imglink'] = img["link"]
        #     yield item
