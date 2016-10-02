# coding:utf-8

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

# 这个url是需要爬取的页面，注意更改这个url的时候下面的for循环里面的url也需要更改
weibo_url = "http://weibo.cn/comment/E70Zv8VNf?uid=2837497737&rl=0&gid=10001#cmtfrm"
# 这里用的是cookies的第一个
res = requests.get(weibo_url, cookies=mcookie[0])
weibo_html = res.text

# 爬取第一页的评论，评论都是在class为c的div里面
comment = bs(weibo_html, 'lxml').find_all('div', class_="c")

for i in range(len(comment)):
    if comment[i].a is None:
        continue
    print "用户ID:", comment[i].a.get('href'), comment[i].a.text
    if comment[i].span is None:
        continue
    print "评论内容:", comment[i].span.text

# 获得评论的页数,用于爬取剩下页面的评论，具有评论页数的信息在class等于pa的div中
pages = bs(weibo_html, 'lxml').find_all('div', class_="pa")

try:
    # 这个是为了获得评论的页数，pages里面是一个字符串，所以就处理了一下
    number_of_pages = pages[0].div.text.split('/')[1][:-1]
except IndexError:
    # 出现这个错误说明只有一页评论
    number_of_pages = 1

for number in range(2, int(number_of_pages)):
    # 修改这个url的时候需要注意将url后面的#cmtfrm删掉
    weibo_url = "http://weibo.cn/comment/E70Zv8VNf?uid=2837497737&rl=0&gid=10001" + "&page=%s" % number

    print weibo_url

    res = requests.get(weibo_url, cookies=mcookie[0])
    weibo_html = res.text
    # 评论都是在class为c的div里面
    comment = bs(weibo_html, 'lxml').find_all('div', class_="c")

    # comment里面的前两个应该是发布者的信息，最后一个是HTML页面的一个信息，都不是用户的评论，所以去掉了
    for i in range(2, len(comment) - 1):
        if comment[i].a is None:
            continue
        print "用户ID:", comment[i].a.text
        if comment[i].span is None:
            continue
        print "评论内容:", comment[i].span.text
