#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: hbcls
# Author:    fan20200225
# Date:      2020/5/17 0017
# -----------------------------------------------------------


class HbCollector(object):
    def __init__(self):
        """
        huaban网图片采集工具。利用browsermobproxy代理服务监听访问huaban采集过程的网络请求，
        提取页面加载过程的.webp格式文件请求，替换为大图链接并进行下载
        """
        pass


if __name__ == "__main__":
    colurl = "https://huaban.com/boards/55182864/"  # huaban采集链接
    # 同一图片的小、大图片链接
    smallpicurl = "http://hbimg.huabanimg.com/7e8999507555859a1d4298fcf575be0afdc9800a1489a-Y07ibn_fw236/format/webp"
    largepicurl = "http://hbimg.huabanimg.com/7e8999507555859a1d4298fcf575be0afdc9800a1489a-Y07ibn_fw236/format/webp"
