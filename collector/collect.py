#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: collector
# Author:    fan20200225
# Date:      2020/5/22 0022
# -----------------------------------------------------------
from dynamichtmlloader import Loader
from htmlparsers import parse_owhat_rank
from make_time_formated import nowtimestr
import sys


def bubsort(datadict: dict) -> list:
    """
    order by value
    :param datadict: {k1:value1, k2:value2, ...}
    :return: sorted datalist 形如[{k1:value1}, {k2:value2}, ...]
    """
    datalist = [{k: datadict[k]} for k in datadict.keys()]
    for i in range(len(datalist) - 1):
        swapped = False
        for j in range(len(datalist) - 1 - i):
            if int(list(datalist[j].values())[0]) < int(list(datalist[j + 1].values())[0]):
                swapped = True
                datalist[j], datalist[j + 1] = datalist[j + 1], datalist[j]
        if not swapped:
            break
    return datalist


def main():
    loader = Loader()
    if sys.platform == "win32":
        loader.config_webdriver(r"C:\WEBDRIVERS\chromedriver.exe")
    if sys.platform == "linux":
        loader.config_webdriver(r"/usr/bin/chromeriver")
    html = loader.load_dynamic_html("https://m.owhat.cn/shop/toplist.html?id=118424")
    rank = parse_owhat_rank(html)
    now = nowtimestr('%Y%m%d%H%M%S')

    # 统计
    nnames = len(rank)
    totalyuan = 0
    top = []
    groups = dict()
    with open("owhat_rank_{}.csv".format(now), "w", encoding="utf-8") as f:  # original data
        for i in range(len(rank)):
            line = "{}, {}, {}".format(i + 1, rank[i]["name"], rank[i]["yuan"])
            # print(line)
            f.write(line + "\n")
            totalyuan += float(rank[i]["yuan"])
            if rank[i]["yuan"] not in groups.keys():
                groups[rank[i]["yuan"]] = 1
            else:
                groups[rank[i]["yuan"]] += 1
            if i in range(20):
                top.append(line)
    lines = [
        "\n统计时间：{}".format(nowtimestr()),
        "\n人数：{}\n总金额：{}".format(nnames, int(totalyuan)),
        "\n\n单个用户金额top20\n排名,用户,金额"
    ]
    for line in top:
        lines.append("\n" + line)
    lines.append("\n\n不同金额选择人数top20\n排名,金额,人数")
    sortedgroups = bubsort(groups)  # 按人数从多到少排序
    for i in range(len(sortedgroups)):
        if i in range(20):
            lines.append("\n{}, {}, {}".format(i+1, *list(sortedgroups[i].items())[0]))
    with open("owhat_data_{}.csv".format(now), "w", encoding="utf-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()
