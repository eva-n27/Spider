# coding:utf-8

import urllib
from my_cookies import getCookies
import requests
from bs4 import BeautifulSoup as bs
import json
import re


def get_html(my_url):
    """
    获得网页的html
    :param my_url: 网页链接
    :return:
    """
    page = urllib.urlopen(my_url)
    my_html = page.read()
    return my_html

# 这个URL是用于登录认证获得cookies的
html = get_html("https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F")
mcookie = getCookies()

# 这个url是需要爬取的页面，注意更改这个url的时候下面的for循环里面的url也需要更改
weibo_url = "http://service.account.weibo.com/show?rid=K1CaO6A5l7agg"
# 这里用的是cookies的第一个
res = requests.get(weibo_url, cookies=mcookie[0])
weibo_html = res.text

str_ = bs(weibo_html, 'lxml').find_all('script')[-6].text
pattern = re.compile(r"{(.|\.)*}")
html_ = re.search(pattern, str_).group(0)
s = json.loads(html_)
for comment in bs(s["html"], 'lxml').find_all('div', class_="con")[1].contents:
    print comment
    print 'end'
