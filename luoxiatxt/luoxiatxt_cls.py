#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: luoxiatxt_cls
# Author:    fan
# date:      2019/11/05
# -----------------------------------------------------------

import os
from requests_html import HTMLSession
import re
import time
from make_time_formated import nowtimestr


NUMS = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9
}
UNITS = {
    "千": 1000,
    "百": 100,
    "十": 10
}


def cnnum2arab(cnnum):
    arab = 0
    if cnnum[0] == "十":
        if cnnum == "十":
            arab = 10
        else:
            arab = 10 + NUMS[cnnum[1]]
    else:
        for i in range(len(cnnum)):
            if cnnum[i] in UNITS.keys():
                arab += NUMS[cnnum[i-1]] * UNITS[cnnum[i]]
            if i == len(cnnum) - 1:
                if cnnum[-1] in NUMS.keys():
                    arab += NUMS[cnnum[-1]]
    return arab


def merge_zhangs(novelpath: str, zhangnames: list):
    # zhangnames：章节列表
    pass


class LuoxiatxtCollector(object):
    def __init__(self):
        self.session = HTMLSession()  # 创建HTML会话实例
        self.website = 'www.luoxia.com'  # 待攻略的网站：落霞小说
        self.url = 'https://' + self.website
        self.novelnames = ['qing']  # 小说名
        self.root = 'D:\\落霞小说_' + re.sub('\D', '', nowtimestr())  # 获取网页资源保存路径, 后缀为当前时间数值
        for tn in self.novelnames:  # 创建保存目录,按小说名
            tn_path = os.path.join(self.root, tn)
            os.makedirs(tn_path)
        self.juans = []
        self.current_novel_folder = None
        self.current_juan_folder = None
        self.current_zhang_name = None

    def match_strings(self, re_exp: str, strings_to_match: list):
        """
        从遍历字符串列表，并与正则表达式匹配，返回符合规则的字符串列表
        :param re_exp:
        :param strings_to_match:
        :return:
        """
        strings_matched = []
        for string in strings_to_match:
            if re.search(re_exp, string):
                strings_matched.append(string)
        return strings_matched

    def intercept_matched_strings(self, re_exp: str, strings_to_intercept: list):
        pattern = re.compile(re_exp, re.S)
        strings_intercepted = []
        for string in strings_to_intercept:
            matched = re.findall(pattern, string)
            if matched:
                strings_to_intercept.append(matched[0])
        return strings_intercepted

    def get_zhang_urls(self, novelname):
        """
        获取某一分类的所有列表页面
        :param novelname:
        :return:
        """
        self.current_novel_folder = os.path.join(self.root, novelname)
        url_novel_home = self.url + '/' + novelname + '/'
        temps = []
        special_temps = []
        response_novel_home = self.session.get(url_novel_home)
        html = response_novel_home.html
        links = html.links
        if links:
            temps = self.match_strings(url_novel_home + '[0-9]+\.htm', links)

        special_attris = html.xpath('body//li/b/attribute::onclick')  # 获取特殊章节
        for attri in special_attris:
            link = attri.split('"')[1]
            special_temps.append(link)
        zhangurls = temps + special_temps
        return zhangurls

    def get_zhang(self, zhang_url):
        """
        获取单页面全部主题的链接
        :param zhang_url: 章节链接
        :return:
        """
        temps = []
        response_page = self.session.get(zhang_url)
        html = response_page.html  # 小说章节页面
        head_text = html.xpath(
            'body/div/header/nav[@id="bcrumb"]')[0].text  # '落霞小说\n落霞小说> 庆余年>第六卷 殿前欢> 第一百五十二章 谁将君心拟火海'
        zhang_text = html.xpath(
            'body/div/article/div[@id="nr1"]')[0].text  # 小说正文
        juan_name = head_text.split('>')[2]  # 获取卷名（作为存储章节.txt的文件夹名）
        zhang_name = head_text.split('>')[3].strip()  # 获取章节名（作为章节.txt的文件名）
        self.current_juan_folder = os.path.join(self.current_novel_folder, juan_name)
        if not os.path.exists(self.current_juan_folder):  # 如果卷文件夹不存在则创建一个卷文件夹
            os.makedirs(self.current_juan_folder)
        # 设置文件名1 获取链接中页面id作为文件名序号（部分章节顺序错误）
        # zhang_id = re.sub('\D', '', zhang_url)
        # self.current_file_name = '{} {}'.format(zhang_id, zhang + '.txt')
        # 设置文件名2 获取章节序号转换为文件名序号（后续组合为单文本文件时进行，此处不重复）
        # try:
        #     zhang_id = re.findall("第\D+章", zhang)[0][1:-1]  # 第二十七章 红袖添香夜抄书"截取中文数字二十七
        #     zhang_id = cnnum2arab(zhang_id)
        # except:
        #     zhang_id = 0
        # self.current_file_name = '{} {}'.format(zhang_id, zhang + '.txt')
        self.current_zhang_name = zhang_name + '.txt'
        return zhang_text  # 章节正文

    def download(self, zhangtext):
        savepath = os.path.join(self.current_juan_folder, self.current_zhang_name)
        with open(savepath, 'w', encoding='utf-8') as f:
            f.write(zhangtext)


if __name__ == '__main__':

    # cnnum2arab中文数字转阿拉伯数字函数测试
    # cn = "十"
    # cn = "十一"
    # cn = "五千零二十一"
    # print(cnnum2arab(cn))

    # **********************************测试下载**********************************
    # qing = LuoxiatxtCollector()
    # urls = qing.get_txtcontent_urls("qing")
    # i = 0
    # for url in urls:
    #     i += 1
    #     if i < 200:
    #         print(url)
            # text = qing.get_txtcontent(url)
            # qing.download(text)
            # time.sleep(0.5)

    # **********************************正式下载**********************************
    qing = LuoxiatxtCollector()
    urls = qing.get_zhang_urls("qing")
    for url in urls:
        try:
            text = qing.get_zhang(url)
            qing.download(text)
            # time.sleep(0.2)
            print('{} 下载成功 {}'.format(qing.current_juan_folder + "\\" + qing.current_zhang_name, url))
        except Exception as e:
            print('{} 下载失败 {} 详情 {}'.format(qing.current_juan_folder + qing.current_zhang_name, url, e))


