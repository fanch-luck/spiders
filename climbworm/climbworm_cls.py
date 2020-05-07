#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: climbworm_cls
# Author:    fan
# date:      2019/11/05
# -----------------------------------------------------------

import os
from requests_html import HTMLSession
import re
import time
from make_time_formated import nowtimestr


class YhxzCollector(object):
    def __init__(self):
        self.session = HTMLSession()  # 创建HTML会话实例
        self.website = 'www.yhxz521.com'  # 待攻略的网站
        self.url = 'http://' + self.website
        self.styles = ['qingchun', 'xinggan', 'siwa', 'hanguo', 'riben', 'xiezhen']  # 分类
        self.style_codes = {'qingchun': 1,  # 分类码，跟分类列表的页面链接有关
                             'xinggan': 2,
                             'siwa': 3,
                             'hanguo': 5,
                             'riben': 6,
                             'xiezhen': 7}
        self.root = 'F:\资源x_' + re.sub('\D', '', nowtimestr())  # 获取网页资源保存路径, 后缀为当前时间数值
        for fl in self.styles:  # 创建保存目录
            fl_path = os.path.join(self.root, fl)
            os.makedirs(fl_path)
        self.current_style = None
        self.current_title = None

    def match_strings(self, re_exp:str, strings_to_match:list):
        strings_matched = []
        for string in strings_to_match:
            if re.search(re_exp, string):
                strings_matched.append(string)
        return strings_matched

    def get_style_pages(self, _style):
        """
        获取某一分类的所有列表页面
        :param _style:
        :return:
        """
        self.current_style = _style
        url_style_homepage = self.url + '/' + _style + '/'
        temps = []
        response_style_homepage = self.session.get(url_style_homepage)
        links = response_style_homepage.html.links
        if links:
            temps = self.match_strings(str(self.style_codes[_style]) + '_[0-9]+\.html', links)
        pages = [url_style_homepage] + [_style + link for link in temps]
        return pages

    def get_title_urls(self, _style, _page):
        """
        获取单页面全部主题的链接
        :param _style:
        :param _page:
        :return:
        """
        temps = []
        response_page = self.session.get(_page)
        links = response_page.html.links
        if links:
            temps = self.match_strings('/' + _style + '/' + '[0-9]+\.html', links)
        title_urls = [self.url + link for link in temps]
        return title_urls

    def get_img_urls(self, title_url):
        pass




if __name__ == '__main__':
    yhxz = YhxzCollector()
    del yhxz
