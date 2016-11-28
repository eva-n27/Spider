# coding: utf-8
# author: Zhengpeng Xiang

import urllib
from my_cookies import getCookies
import requests
from bs4 import BeautifulSoup as bs


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

# 需要爬取的页数
pages = 10

# 将这个用户说的话存放在这里
data = []

for page in range(1, pages + 1):
    # 这个url是需要爬取的页面
    # 首先在网页端打开需要爬取的人的url，比如杨幂的是http://weibo.com/yangmiblog?refer_flag=1001030101_
    # 将weibo.com改成weibo.cn，其他不变
    # 然后在打开的页面里面点下一页，就可以看到在url后面变成了?page=页数，然后修改成下面这个url
    weibo_url = "http://weibo.cn/yangmiblog?page=%s" % page

    # 这里用的是cookies的第一个地方,使用cookie去访问这个网页
    res = requests.get(weibo_url, cookies=mcookie[0])
    weibo_html = res.text

    # find_all返回的是class为ctt的span的列表，名称在第一个span里
    user_name = bs(weibo_html, 'lxml').find_all('span', class_="ctt")[0].text.split()[0]



    # 找到发的微博
    weibos = bs(weibo_html, 'lxml').find_all('div', class_='c')
    for weibo in weibos:
        # 如果存在cmt的span，则是转发的内容
        if weibo.find('span', class_='cmt'):
            # 这种情况下，应该爬取转发理由，转发理由在class为c的div下的第二个div里面
            text = weibo.find_all('div')[1].text.split()[0]
            data.append(text)
        elif weibo.find('span', class_='ctt'):
            # 这种情况下，应该爬取微博正文，微博正文在class为c的div下的第一个div里面，所以用find就行
            text = weibo.find('span', class_='ctt').text
            data.append(text)

for item in data:
    print item
