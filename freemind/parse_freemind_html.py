#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: parse_freemind_html
# Author:    fan20200225
# Date:      2020/7/12 0012
# -----------------------------------------------------------

from lxml import etree
import os

def parse_freemind_html(htmlfile):
    assert os.path.exists(htmlfile)
    with open(htmlfile, 'r') as hf:
        html = hf.read()
    tree = etree.HTML(html)
    titlexpath = '/html/body/p/span/text()'
    casexpath = '/html/body/ul/li/span/text()'
    forwordxpath = '/html/body/ul/li/ul/li/span/text()'
    stepxpath = '/html/body/ul/li/ul/li/ul/li/span/text()'
    expectxpath = '/html/body/ul/li/ul/li//ul/li/ul/li/span/text()'

    casesxpath = '/html/body/ul/li[1]/span'  # 第一个用例名
    casesxpath = '/html/body/ul/li[1]/ul/li[1]/span'  # 第一个用例的前置条件
    casesxpath = '/html/body/ul/li[1]/ul/li[1]/ul/li[1]/span'  # 第一个用例的第一个步骤
    casesxpath = '/html/body/ul/li[1]/ul/li[1]/ul/li[1]/ul/li[1]/span'  # 第一个用例的第一个步骤的预期
    casesxpath = '/html/body/ul/li[3]/ul/li[1]/ul/li[2]/ul/li[1]/span'  # 第3个用例的第2个步骤的预期（无）
    n_cases = len(tree.xpath('/html/body/ul/li/span'))  # 某模块的用例数
    n_steps = len(tree.xpath('/html/body/ul/li[3]/ul/li[1]/ul/li/span'))  # 用例3的步骤数

    # print(tree.xpath(titlexpath))
    # print(tree.xpath(casexpath))
    # print(tree.xpath(forwordxpath))
    # print(tree.xpath(stepxpath))
    # print(tree.xpath(expectxpath))
    spans = tree.xpath('/html/body/ul/li/span/text()')
    print("用例数 {}, 用例的步骤数 {}.".format(n_cases, n_steps))
    for span in spans:
        print(span)


if __name__ == "__main__":
    hp = r"D:\fan20200225\Documents\模块名.mm.html"
    parse_freemind_html(hp)
