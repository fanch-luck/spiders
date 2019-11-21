#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: get_yhxz
# Author:    fan
# date:      2019/10/31
# -----------------------------------------------------------
import os
from requests_html import HTMLSession
import re
import time
from make_time_formated import nowtimestr


def get_title_list_pages(fenlei):
    global fenlei_codes
    global path_fenlei
    global url_fenlei
    global path_title
    title_list_urls = []  # 标题列表页面链接
    url_fenlei = url + '/' + fenlei + '/'
    r_fenlei = session.get(url_fenlei)  # 请求页面-分类页
    path_fenlei = os.path.join(root, fenlei)
    os.mkdir(path_fenlei)  # 创建保存路径下分类文件夹+
    links = r_fenlei.html.links
    while links:
        link = links.pop()
        if re.search(str(fenlei_codes[fenlei]) + '_[0-9]+\.html', link):  # 匹配各个页码对应链接
            title_list_urls.append(url_fenlei + link)
    title_list_urls.append(url_fenlei)  # 将分类首页包含进列表
    return title_list_urls


def get_title_urls(_fenlei, title_list_url):
    title_urls = []  # 保存标题页面链接
    r_title_list = session.get(title_list_url)
    for link in r_title_list.html.links:  # 获取分类下的各个标题首页链接并保存到list
        if re.search('/' + _fenlei + '/' + '[0-9]+\.html', link):
            link = url + link
            title_urls.append(link)
    return title_urls


def get_img_urls(title_url):
    global path_fenlei
    global url_fenlei
    global path_title
    img_urls = []
    r_title = session.get(title_url)
    elems = r_title.html.xpath('/html/head/title')
    page_title = elems[0].text  # 获取标题文本
    title = page_title.split('-')[0]
    path_title = os.path.join(path_fenlei, re.sub('\D', '', nowtimestr()) + ' ' + title)
    os.mkdir(path_title)  # 创建分类目录下的标题文件夹
    base_num = title_url.split('/')[-1].split('.')[0]  # 获取基准数字，该标题下所有文件所在页面的url末端均以此为前缀，正则匹配用
    for link in r_title.html.links:
        if re.search(base_num + '_[0-9]*.html', link):
            link = url_fenlei + '/' + link
            img_urls.append(link)
    img_urls.append(title_url)  # 将标题首页包含进列表
    return img_urls


def download_file(_img_url, save_to):
    r = session.get(_img_url)
    elems = r.html.xpath('//*[@id="bigimg"]')  # 匹配图片元素
    elem_src = elems[0].attrs['src']
    img_real_url = url + elem_src  # 组装文件绝对url
    img_fmt = os.path.splitext(img_real_url)[-1]
    r_img = session.get(img_real_url)  # 获取文件（字节码流）
    img = r_img.html.raw_html
    file_name = r.html.url.split('/')[-1].split('.')[0]  # 设置文件名
    file_path = os.path.join(save_to, file_name + img_fmt)
    # f = open(file_path, 'wb')
    # f.write(img)  # 下载当前文件
    # f.close()
    return img, file_path


def save_files(img_save_dic: dict):
    """
    集中保存文件，减少硬盘写频率
    :param img_save_dic:
    :return:
    """
    # f_list = []
    for key in img_save_dic.keys():
        file_path = key
        img = img_save_dic[file_path]
        try:
            f = open(file_path, 'wb')
            # f_list.append(f)
            f.write(img)  # 下载当前文件
            f.close()
        except Exception:
            print('an error happened while downloading {}'.format(key))
            continue


if __name__ == '__main__':
    session = HTMLSession()
    website = 'www.yhxz521.com'  # 待攻略的网站
    url = 'http://' + website
    fenleis = ['qingchun', 'xinggan', 'siwa', 'hanguo', 'riben', 'xiezhen']  # 分类
    fenlei_codes = {'qingchun': 1,
                    'xinggan': 2,
                    'siwa': 3,
                    'hanguo': 5,
                    'riben': 6,
                    'xiezhen': 7}
    root = 'F:\资源_' + re.sub('\D', '', nowtimestr())  # 获取网页资源保存路径, 后缀为当前时间数值
    os.mkdir(root)
    url_fenlei = None
    path_fenlei = None
    path_title = None

# ************************下载测试*******************************
#     fl = fenleis[3]
#     title_list_pages = get_title_list_pages(fl)
#     print('获取分类下所有标题列表页面链接：')
#     print(title_list_pages)
#     list_url = title_list_pages[0]
#     title_urls = get_title_urls(fl, list_url)
#     print('  获取列表页面所有标题页链接：')
#     print(title_urls)
#     title_url = title_urls[0]
#     img_urls = get_img_urls(title_url)
#     print('    获取文件页面链接')
#     print(img_urls)
#     img_url = img_urls[0]
#     download_file(img_url, path_title)

#  ************************正式下载*******************************
    for fl in fenleis:
        for title_list_page in get_title_list_pages(fl):
            for title_url in get_title_urls(fl, title_list_page):
                file_save_dic = {}
                for img_url in get_img_urls(title_url):
                    try:
                        file_written, file_path = download_file(img_url, path_title)
                        file_save_dic[file_path] = file_written
                        print(img_url + ' --> ' + path_title)
                        time.sleep(0.1)
                    except Exception:
                        print('an error happened while downloading {}'.format(img_url))
                        time.sleep(0.1)
                        continue
                save_files(file_save_dic)
                print('title saved --> ' + fl + ': ' + title_url)
