#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: collector
# Author:    fan20200225
# Date:      2020/5/22 0022
# -----------------------------------------------------------
from collector.dynamichtmlloader import Loader
from collector.htmlparsers import parse_owhat_rank


def main():
    loadder = Loader()
    loadder.config_webdriver(r"C:\WEBDRIVERS\chromedriver.exe")
    html = loadder.load_dynamic_html("https://m.owhat.cn/shop/toplist.html?id=100944")
    parse_owhat_rank(html)


if __name__ == "__main__":
    main()
