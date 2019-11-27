# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time


class WeiboimgscollectorDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"C:\WEBDRIVERS\chromedriver.exe")

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        if '.jpg' not in request.url:
            self.driver.get(request.url)
            # current_scrollheight = 0
            # while current_scrollheight != self.driver.execute_script("return document.body.scrollHeight"):
            #     try:
            #         current_scrollheight = self.driver.execute_script("return document.body.scrollHeight")
            #         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            #         time.sleep(3)
            #     except TimeoutException:
            #         print('middlewares.WbmgsSpiderMiddleware.process_request: 超时')
            #         self.driver.execute_script('window.stop()')
            time.sleep(2)
            html = self.driver.page_source

            # f = open("source.html", 'w', encoding='utf-8')
            # f.write(html)
            # time.sleep(1)
            # f.close()

            self.driver.quit()
            body_htmlresponse = html.encode('utf-8')
            return HtmlResponse(url=request.url, body=body_htmlresponse, encoding='utf-8', request=request)
