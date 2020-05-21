#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: wbcls
# Author:    fan20200225
# Date:      2020/5/16 0016
# -----------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import re
import os
from requests_html import HTMLSession  # 用于下载文件
from make_time_formated import *
from lxml import etree  # 解析html文本


class WbCollector(object):
    def __init__(self, webdriverpath):
        """
        使用selenium动态读取wb页面并搜集图片
        """
        self.webdriverpath = webdriverpath
        self.sesion = HTMLSession()  # 创建对话实例
        self.driver = None
        self.html = None
        self.base_url = None

        self.config_driver()

    def config_driver(self):
        """
        配置webdriver
        :return:
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=self.webdriverpath)

    def load_dynamic_page(self, wburl: str) -> str:
        """
        使用selenium完整加载动态页面
        :param wburl:
        :return: html页面文件（字符串）
        """
        self.driver.get(wburl)
        current_scrollheight = 0
        while current_scrollheight != self.driver.execute_script("return document.body.scrollHeight"):
        # while current_scrollheight < 3: # test
        #     current_scrollheight -= 1
            try:
                current_scrollheight = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
            except TimeoutException:
                print('load wb page time out.')
                self.driver.execute_script('window.stop()')
        time.sleep(1)
        html = self.driver.page_source
        self.driver.quit()
        self.html = html
#         self.base_url = html.base_url
        # with open("html.html", "w", encoding="utf-8") as f:
        #     f.write(html)
        return html

    def parse_wb_page(self, htmlsource: str) -> list:
        """
        使用xpath进行页面解析，获取图片相关信息，按数据结构组合并返回
        :param htmlsource: html文本（str）
        :return: 含图片链接的数据结构
        """
        tree = etree.HTML(htmlsource)
        cardxpath = '//article'  # 匹配所有微博‘卡片’路径
        textxpath = 'div/div/text()'  # 匹配当前微博卡片下微博文本
        imgurlxpath = 'div[@class="weibo-og"]//img/attribute::src'  # 匹配当前微博卡片下所有图片（含无用图）
        # src_urls = tree.xpath('//article//div[@class="weibo-og"]//li[@class="m-auto-box"]//img/attribute::src')
        cards = tree.xpath(cardxpath)
        wbimg_data = []
        imgdic = dict()
        for card in cards:
            dic = imgdic.copy()
            texts = card.xpath(textxpath)
            imgurls = card.xpath(imgurlxpath)
            # print(texts)
            # print(imgurls)
            if len(imgurls) >= 1:
                imgname = "".join([re.sub('[\\\/?*:><|\"]+', "", text) for text in texts]).strip()
                imgurls = [url.replace("orj360", "large") for url in imgurls if url.endswith(".jpg")]
                dic["name"] = imgname
                dic["urls"] = imgurls
                wbimg_data.append(dic)
        return wbimg_data

    def download_img(self, imgurl: str) -> bytes:
        """
        下载图片
        :param imgurl: 图片链接
        :return:
        """
        if imgurl.endswith(".jpg"):
            resp = self.sesion.get(imgurl)
            return resp.html.raw_html

    def save_img(self, imgdata, outputpath=None):
        """
        保存图片
        :param outputpath: 保存路径
        :return:
        """
        pass

    def download_imgs(self, wbimgdata:list, downloadpath) -> None:
        """
        下载图片
        :param imgurls: 下载链接列表
        :param downloadpath: 下载目录
        :return:
        """
        savedata = []
        savedic = dict()
        print("start downloading images")
        for imgs in wbimgdata:
            if len(imgs) == 2:
                # print(imgs)
                title = imgs["name"]
                if len(imgs["name"]) >= 30:
                    title = imgs["name"][:30]
                for i in range(len(imgs["urls"])):
                    dic = savedic.copy()
                    dic["savepath"] = "{}\\{}_{}.jpg".format(downloadpath, title, i)
                    # dic["imgurl"] = imgs["urls"][i]
                    dic["imgdata"] = self.download_img(imgs["urls"][i])
                    print("file downloaded: {}".format(imgs["urls"][i]))
                    savedata.append(dic)
        print("downloading finished.\nnow start to save files")
        for i in savedata:
            # print("{}_{}".format(i["savepath"], i["imgurl"]))
            with open(i["savepath"], "wb") as f:
                f.write(i["imgdata"])


def single_download(wburl, downloadpath) -> None:
    if not os.path.exists(downloadpath):
        os.makedirs(downloadpath)
    wb = WbCollector(WEBDRIVERPATH)
    html = wb.load_dynamic_page(wburl)
    wb_img_data = wb.parse_wb_page(html)
    wb.download_imgs(wb_img_data, downloadpath)


def multi_download(picstations: list) -> None:
    if picstations:
        for item in picstations:
            downloadpath = os.path.join(base_path, item["name"])
            wburl = item["url"]
            single_download(wburl, downloadpath)


if __name__ == "__main__":
    WEBDRIVERPATH = r"C:\WEBDRIVERS\chromedriver.exe"
    base_path = r"E:\火箭少女101\YCY图片"

    picfolder = "杨超越的摸鱼基地"
    download_path = os.path.join(base_path, picfolder)
    wb_url = "https://m.weibo.cn/u/7165916155?uid=7165916155&luicode=10000011&lfid=1076037165916155"
    # single_download(wb_url, download_path)

    YCYPICSTATIONS = [
    {"name": "散仙丨杨超越个站",
     "url": "https://m.weibo.cn/u/5324768697?uid=5324768697&luicode=10000011&lfid=1076035324768697"},
    {"name": "whYUEspecial·杨超越",
     "url": "https://m.weibo.cn/u/2676540645?uid=2676540645&luicode=10000011&lfid=1008082a98366b6a3546bd16e9da0571e34b84_-_soul"},
    {"name": "ChampagneRose_杨超越个站",
     "url": "https://m.weibo.cn/u/5951606667?uid=5951606667&luicode=10000011&lfid=1076035951606667"},
    {"name": "杨超越的摸鱼基地",
     "url": "https://m.weibo.cn/u/7165916155?uid=7165916155&luicode=10000011&lfid=1076037165916155"},
    {"name": "SweetTown0731_杨超越",
     "url": "https://m.weibo.cn/u/6573230444?uid=6573230444&luicode=10000011&lfid=1076036573230444"},
    {"name": "l绝对甜度l-杨超越奶糖个站",
     "url": "https://m.weibo.cn/u/6675007997?uid=6675007997"},
    {"name": "Pirateship_杨超越",
     "url": "https://m.weibo.cn/u/7261549951?uid=7261549951&luicode=10000011&lfid=1076037261549951"},
    {"name": "杨超越FashionChannel",
     "url": "https://m.weibo.cn/u/6457609902?uid=6457609902&luicode=10000011&lfid=1076036457609902"},
    {"name": "初·拾吾丨杨超越个站",
     "url": "https://m.weibo.cn/u/6874700984?uid=6874700984&luicode=10000011&lfid=1076036874700984"},
    {"name": "FancyCarp-杨超越锦鲤站",
     "url": "https://m.weibo.cn/u/6841492211?uid=6841492211&luicode=10000011&lfid=1076036841492211"},
    {"name": "·731号星球·",
     "url": "https://m.weibo.cn/u/6349247329?uid=6349247329&luicode=10000011&lfid=1076036349247329"}
]
    # multi_download(YCYPICSTATIONS)
