# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import re
import time
from requests_html import HTMLSession
from scrapy.http import HtmlResponse


# class Ff96CollectorSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


class Ff96CollectorDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls()
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s

    def process_request(self, request, spider):

        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        if re.match('https://96ff.net/luyilu/list_5_[0-9]+.html', request.url):
            # 返回主题列表页面，解析网页并获取标题链接
            print('正在该页面解析标题列表地址, {}'.format(request.url))
            session = HTMLSession()
            response = session.get(request.url).html
            time.sleep(0.5)
            for elem in response.xpath('//article/header/h2/a'):
                # print(elem)
                # print(elem.xpath('//attribute::href'))
                imglisthomeurl = 'https://96ff.net' + elem.xpath('//attribute::href')[0]
                shorturl = imglisthomeurl.split('/')[-1]
                basenum = shorturl.split('.')[0]
                imgpageurls = [imglisthomeurl]
                for i in range(2, 5):
                    newshorturl = '/' + basenum + '_' + str(i) + '.html'
                    imglisturl = re.sub('/[0-9]+.html', newshorturl, imglisthomeurl)  # 拼接文件列表页面url
                    imgpageurls.append(imglisturl)
                for imglisturl in imgpageurls:
                    session = HTMLSession()
                    respnse = session.get(imglisturl).html
                    time.sleep(0.2)
                    htmlresponse = HtmlResponse(url=imglisturl, body=response,
                                                encoding='utf-8', )
                    yield respnse

        if re.match('https://96ff.net/luyilu/[0-9]+_*[0-9]*.html', request.url):
            # 返回文件列表页面，解析网页并获取图片链接
            print('正在该页面解析文件列表 , {}'.format(request.url))




    # def process_response(self, request, response, spider):
    #     # Called with the response returned from the downloader.
    #
    #     # Must either;
    #     # - return a Response object
    #     # - return a Request object
    #     # - or raise IgnoreRequest
    #     return response
    #
    # def process_exception(self, request, exception, spider):
    #     # Called when a download handler or a process_request()
    #     # (from other downloader middleware) raises an exception.
    #
    #     # Must either:
    #     # - return None: continue processing this exception
    #     # - return a Response object: stops process_exception() chain
    #     # - return a Request object: stops process_exception() chain
    #     pass
    #
    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)
