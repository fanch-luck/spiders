#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: photocollector
# Author:    fan20200225
# Date:      2020/9/26 0026
# -----------------------------------------------------------

from lxml import etree
from requests_html import HTMLSession
import re
import os
import time


class PhotoCollector(object):
    def __init__(self):
        self.session = HTMLSession()
        self.debug = 1

    def hit_urls(self, re_exp: str, strings_to_match: list):
        if self.debug:
            print(re_exp)
        strings_matched = []
        for string in strings_to_match:
            if re.search(re_exp, string):
                strings_matched.append(string)
        return strings_matched

    def photo_style_frontpage(self, baseurl, photostyle):
        url = baseurl + "/" + photostyle
        pagenumid = "page num id is None"
        for item in STYLES:
            if item["style"] == photostyle:
                pagenumid = item["pagenumid"]
        albumurl_re = "[\d]{1,5}"
        pagenum_re = "list_" + pagenumid + "_[\d]{1,4}"

        response = self.session.get(url)
        links = response.html.links

        albumrls = self.hit_urls(url + "/" + albumurl_re, links)
        pagenumurls = self.hit_urls("/" + pagenum_re + ".html", links)
        if self.debug:
            print("album links and page number links")
            print(albumrls)
            print(pagenumurls)


if __name__ == "__main__":
    STYLES = [
        {"style": "xinggan", "description": "1", "pagenumid": "1"},
        {"style": "qingchun", "description": "2", "pagenumid": "2"},
        {"style": "xiaohua", "description": "3", "pagenumid": "3"},
        {"style": "chemo", "description": "4", "pagenumid": "4"},
        {"style": "qipao", "description": "5", "pagenumid": "5"},
        {"style": "mingxing", "description": "6", "pagenumid": "6"},
        {"style": "zhuanti", "description": "7", "pagenumid": "7"},
    ]
    pc = PhotoCollector()
    pc.photo_style_frontpage("http://www.mm131.vip", "xinggan")
