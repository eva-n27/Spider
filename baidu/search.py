# coding: utf-8
# author: Zhengpeng Xiang
# date: 2017/07/26

import urllib
import urllib2
import requests
from bs4 import BeautifulSoup as bs
import re


def get_html(keywords_):
    """
    获得网页的html
    from https://github.com/fancoo/BaiduCrawler/blob/master/baidu_crawler.py
    :return:
    """
    key = {'wd': keywords_}

    # 请求Header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0 cb) like Gecko'}

    # 抓取数据内容
    web_content = requests.get("https://www.baidu.com/s?", params=key, headers=headers, timeout=4)

    return web_content.text


def html_parser(html_):
    """
    解析html
    """
    soup_ = bs(html_, 'lxml').find('div', id="content_left")

    # 找到所有class为c-abstract的div
    # 分析了一下，只有这个标签中的数据是我们需要的文本
    # 然后可以再去爬一下百度百科
    c_abstract_ = soup_.find_all('div', class_="c-abstract")

    # 设置返回结果
    text_ = []

    # 提取数据
    if len(c_abstract_) != 0:
        for item_ in c_abstract_:
            text_.append(item_.text.strip())

    return text_

html = get_html('游戏名')
text = html_parser(html)
