#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: collector
# Author:    fan20200225
# Date:      2020/5/22 0022
# -----------------------------------------------------------
from lxml import etree  # 解析html文本
import re


def parse_wb_page(htmlsource: str) -> list:
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


def parse_owhat_rank(htmlsource: str) -> None:
    tree = etree.HTML(htmlsource)
    eachonexpath = '//div[@class="each_one"]'
    eachonenamepath = "div/h2/text()"
    eachoneyuanpath = "div/h2/cite/text()"
    eachones = tree.xpath(eachonexpath)
    rank = []
    for eachone in eachones:
        record = dict().copy()
        record["name"] = eachone.xpath(eachonenamepath)[0]
        record["yuan"] = eachone.xpath(eachoneyuanpath)[0]
        rank.append(record)
    with open("owhat_rank.csv", "w", encoding="utf-8") as f:
        for i in range(len(rank)):
            line = "{}, {}, {}".format(i + 1, rank[i]["name"], rank[i]["yuan"])
            print(line)
            f.write(line + "\n")


if __name__ == "__main__":
    pass
