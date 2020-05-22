#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: dynamichtmlloader
# Author:    fan20200225
# Date:      2020/5/22 0022
# -----------------------------------------------------------
from requests_html import HTMLSession  # 用于下载文件
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import os
import time


class Loader(object):
    def __init__(self):
        self.webdriver = None
        self.driver = None
        self.html = None
        self.base_url = None

    def config_webdriver(self, webdriverpath):
        if os.path.isfile(webdriverpath):
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=webdriverpath)

    def load_dynamic_html(self, url: str) -> str:
        """
        使用selenium完整加载动态页面
        :param url:
        :return: html页面文件（字符串）
        """
        if url:
            self.driver.get(url)
            current_scrollheight = 0
            while current_scrollheight != self.driver.execute_script("return document.body.scrollHeight"):
                # while current_scrollheight < 3: # test
                #     current_scrollheight -= 1
                try:
                    current_scrollheight = self.driver.execute_script("return document.body.scrollHeight")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    print('now loading wb page...', current_scrollheight)
                    time.sleep(2)
                except TimeoutException:
                    print('load wb page time out.')
                    self.driver.execute_script('window.stop()')
            time.sleep(1)
            html = self.driver.page_source
            self.driver.quit()
            # self.base_url = html.base_url
            # with open("html.html", "w", encoding="utf-8") as f:
            #     f.write(html)
            return html


if __name__ == "__main__":
    pass
