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

        self.index_m3u8_url = None
        self.indexm3u8 = None
        self.ts_base_url = None  # ts文件存放路径的base URL
        self.ts_urls = []
        self.tss = dict()

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

    def get_index_m3u8_url(self, videoplayurl):
        self.proxy.new_har("demo", options={'captureHeaders': True, 'captureContent': True})  # 创建HAR文件
        # HAR是记录http请求发出直到收到完整的响应所发生的http交互细节（url、响应时间等等）的标准化工具
        self.driver.get(videoplayurl)
        time.sleep(5)
        har = self.proxy.har
        # f = open("har.js", "w", encoding="utf-8")
        # f.write(har)
        # time.sleep(1)
        # f.close()
        entries = har["log"]["entries"]  # 提取http请求和响应条目(结构参看har.js文件)
        indexm3u8_url = None

        for entry in entries:
            if "index.m3u8" in entry["request"]["url"]:
                if entry["response"]["status"] == 200:
                    indexm3u8_url = entry["request"]["url"]
                    print("index.m3u8 found!")
                    break
        if not indexm3u8_url:
            print("index.m3u8 no found!")
        self.index_m3u8_url = indexm3u8_url

    def get_index_m3u8(self):
        indexm3u8 = None
        ts_base_url = None
        if self.index_m3u8_url:
            response = self.session.get(self.index_m3u8_url)  # index.m3u8文件下载
            indexm3u8 = response.html.html
            print("index.m3u8 url: " + self.index_m3u8_url)
            print("index.m3u8 文件内容: \n" + indexm3u8)
            m = re.search("\S+.com", self.index_m3u8_url)  # base url https://605ziyuan.com
            ts_base_url = m.group()
        self.ts_base_url = ts_base_url
        self.indexm3u8 = indexm3u8

    # html = self.driver.page_source
    # f = open("demo.html", "w", encoding="utf-8")
    # f.write(html)
    # time.sleep(1)
    # f.close()

    def get_ts_m3u8_urls(self):
        global ts_url
        if self.ts_base_url and self.indexm3u8:
            lines = self.indexm3u8.split("\n")
            for line in lines:
                if ".m3u8" in line:
                    if ("https://" in line) or ("http://" in line):
                        tsm3u8_url = line
                    else:
                        m = re.search("/\S+.m3u8", line)  # relative path /ppvod/RuIp5mQv.m3u8
                        if not m:
                            print("parse index.m3u8 failed, fail to get url of ts links m3u8")
                            break
                        else:
                            tsm3u8_url = self.ts_base_url + m.group()
                            print(".m3u8 found!")
                    response = self.session.get(tsm3u8_url)  # 包含ts文件链接的.m3u8文件下载
                    tsm3u8 = response.html.html
                    print(".m3u8 url: " + tsm3u8_url)
                    print(".m3u8 文件内容: \n" + tsm3u8)
                    lines = tsm3u8.split("\n")

                    for line in lines:
                        ts_url = None
                        if ".ts" in line:
                            if ("https://" in line) or ("http://" in line):
                                ts_url = line
                            else:
                                m = re.search("/\S+.ts", line)  # relative path /20180506/zDOacWsg/800kb/hls/rzEv2825000.ts
                                if not m:
                                    print("parse .m3u8 failed, fail to get url of ts files")
                                else:
                                    ts_url = self.ts_base_url + m.group()
                            print(ts_url)
                            self.ts_urls.append(ts_url)

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

    def save_ts_file(self, ts_name, ts_data):
        if ts_name and ts_data:
            try:
                file = open(ts_name, "wb", )
                file.write(ts_data)
                file.close()
                print("ts file {} saved.".format(ts_name))
            except Exception as e:
                print("save ts file failed. detail: {}".format(e))

    def download_ts_files(self):
        if self.ts_urls:
            tsurls = sorted(self.ts_urls)
            for tsurl in tsurls:
                if tsurl:
                    ts_name, ts_data = self.download_ts_data(tsurl)
                    self.tss[ts_name] = ts_data
                    time.sleep(0.1)
            time.sleep(1)
            tsdatas = []
            for k in sorted(self.tss.keys()):
                tsdatas.append(self.tss[k])
            data = b''.join(tsdatas)
            self.save_ts_file("video.mp4", data)


    def merge_ts_files(self):
        pass


if __name__ == "__main__":
    webdriver_path = r"C:\WEBDRIVERS\chromedriver.exe"
    browsermob_proxy_bat_path = r"E:\MyWorkPlace\spiders\browsermob-proxy\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat"
    video_play_url = "http://www.zd518.cn/vod-play-id-142752-src-1-num-1.html"
    collector = M3uCllector(webdriver_path, browsermob_proxy_bat_path)
    collector.get_index_m3u8_url(video_play_url)
    collector.get_index_m3u8()
    collector.get_ts_m3u8_urls()
    collector.download_ts_files()
    # tsname, tsdata = collector.download_ts_data(collector.ts_urls[0])
    # print("tsname, tsdata")
    # collector.save_ts_file(tsname, tsdata)

