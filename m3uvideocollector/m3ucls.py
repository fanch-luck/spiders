#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: m3ucls
# Author:    fan20200225
# Date:      2020/5/5 0005
# -----------------------------------------------------------

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import re
from requests_html import HTMLSession  # 用于下载文件
from browsermobproxy import Server
from make_time_formated import *
import _thread as thread
# browsermobproxy 是基于LittleProxy的的代理服务，启用时作为，作为Selenium浏览器的标准代理，抓取请求和返回内容
# 需下载脚本文件配合用https://github.com/lightbody/browsermob-proxy/releases


class M3uCllector(object):
    def __init__(self, wbdriverpth, browsermobproxybatpath):
        self.webdriverpath = wbdriverpth
        self.driver = None

        self.browsermob_proxy_bat_path = browsermobproxybatpath
        self.proxy_server = None
        self.proxy = None

        self.session = HTMLSession()

        self.m3u8_urls = None
        self.ts_base_url = None  # ts文件存放路径的base URL
        self.ts_urls = []
        self.tsdata = dict()

        self.config_driver()  # 初始化webdriver和browsermob_proxy服务器

    def config_driver(self):
        self.proxy_server = Server(self.browsermob_proxy_bat_path)  # 实例化代理服务器（需Java支持）
        self.proxy_server.start()
        self.proxy = self.proxy_server.create_proxy()

        chrome_options = Options()
        chrome_options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))  # 将代理服务器设置添加到chrome设置
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=self.webdriverpath)

    def get_m3u8_urls(self, videoplayurl):
        """
        监听HTTP响应结果，找出.m3u8链接
        :param videoplayurl: 视频播放页面URL
        :return: m3u8链接（列表）
        """
        self.proxy.new_har("demo", options={'captureHeaders': True, 'captureContent': True})  # 创建HAR文件
        # HAR是记录http请求发出直到收到完整的响应所发生的http交互细节（url、响应时间等等）的标准化工具
        self.driver.get(videoplayurl)
        time.sleep(5)
        har = self.proxy.har
        # f = open("har.js", "w", encoding="utf-8")
        # f.write(har)
        # time.sleep(1)
        # f.close()

        # html = self.driver.page_source
        # f = open("page_source.html", "w", encoding="utf-8")
        # f.write(html)
        # time.sleep(1)
        # f.close()

        entries = har["log"]["entries"]  # 提取http请求和响应条目(结构参看har.js文件)
        m3u8_urls = []
        for entry in entries:
            if entry["request"]["url"].endswith(".m3u8"):  # 提取.m3u8链接
                if entry["response"]["status"] == 200:
                    print("m3u8 url found: " + entry["request"]["url"])
                    m3u8_urls.append(entry["request"]["url"])
        if not m3u8_urls:
            print("m3u8 url no found!")
        self.m3u8_urls = m3u8_urls
        return m3u8_urls

    def get_ts_urls(self, m3u8urls: list, tsbaseurl=None):
        ts_base_url = tsbaseurl
        ts_urls = []
        if not m3u8urls:
            print("please input a list of urls")
        else:
            for m3u8url in m3u8urls:
                response = self.session.get(m3u8url)  # index.m3u8文件下载
                m3u8 = response.html.html
                print("m3u8 url: " + m3u8url)
                print("parsing .m3u8: \n" + m3u8)
                lines = m3u8.split("\n")
                for line in lines:
                    if line.endswith(".ts"):
                        print(line)
                        ts_urls.append(line)
                if ts_urls:
                    if not ts_base_url:
                        ts_base_url = "/".join(m3u8url.split("/")[:-1])  # 最大可能匹配存放m3u8和ts文件的路径
                else:
                    print(".m3u8 file parsed, but fail to get url of ts files")
        # print(ts_base_url)
        # print(ts_urls)
        if ts_base_url and ts_urls:
            ts_urls = [ts_base_url + "/" + url for url in ts_urls]  # 合并成完整ts URL
        self.ts_base_url = ts_base_url
        self.ts_urls = ts_urls
        return ts_urls

    def download_ts_data(self, tsurl):
        ts_name = None
        ts_data = None
        if tsurl:
            response = self.session.get(tsurl)
            ts_name = tsurl.split('/')[-1]
            ts_data = response.html.raw_html
            print(tsurl)
            print(ts_name)
            # print(ts_data)
        return ts_name, ts_data

    def save_ts_file(self, tssavepath, tsdata):
        if tssavepath and tsdata:
            try:
                file = open(tssavepath, "wb", )
                file.write(tsdata)
                file.close()
                print("file {} saved.".format(tssavepath))
            except Exception as e:
                print("save file failed. detail: {}".format(e))

    def download_ts_files(self, tsurls=None, savepath=""):
        if not tsurls:
            ts_urls = self.ts_urls
        else:
            ts_urls = tsurls
        if ts_urls:
            # for tsurl in ts_urls:
            #     if tsurl:
            #         ts_name, ts_data = self.download_ts_data(tsurl)
            #         self.tsdata[ts_name] = ts_data
            #         time.sleep(0.1)
            for i in range(len(ts_urls)):
                if ts_urls[i]:
                    self.tsdata[i] = {"url": ts_urls[i]}
            for k in self.tsdata.keys():
                self.tsdata[k]["name"], self.tsdata[k]["data"] = \
                    thread.start_new(self.download_ts_data, (self, self.tsdata[k]["url"]))
                time.sleep(1)
            time.sleep(1)
            tsdatas = []
            for k in sorted(self.tsdata.keys()):
                tsdatas.append(self.tsdata[k]["data"])
            data = b''.join(tsdatas)
            if not savepath:
                sp = nowtimestr("%Y%m%d%H%M%S") + ".mp4"
            else:
                sp = savepath + "\\" + nowtimestr("%Y%m%d%H%M%S") + ".mp4"
            self.save_ts_file(sp, data)

    def merge_ts_files(self, tsfilespath: str):
        """
        merge ts files to a video
        :param tsspath: path that contains several ts files
        :return:
        """
        pass


if __name__ == "__main__":
    webdriver_path = r"C:\WEBDRIVERS\chromedriver.exe"
    browsermob_proxy_bat_path = r"E:\MyWorkPlace\spiders\browsermob-proxy\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat"
    video_play_url = "https://www.555duo.net/a/play1/7633.html"
    collector = M3uCllector(webdriver_path, browsermob_proxy_bat_path)
    m3u8_urls = collector.get_m3u8_urls(video_play_url)
    # m3u8_urls = ["https://2.ddyunbo.com/20191219/2V4EJdvv/800kb/hls/index.m3u8"]
    ts_urls = collector.get_ts_urls(m3u8_urls)
    output = r"E:\MyWorkPlace\spiders\m3uvideocollector\download"
    collector.download_ts_files(ts_urls, output)

