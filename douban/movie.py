# coding: utf-8
# author: Zhengpeng Xiang
# date: 2016/10/02

import urllib
import demjson
from initDatabase import cur, conn

douban_class = ['热门', '最新', '经典', '豆瓣高分', '动作', '喜剧', '爱情', '华语', '欧美', '韩国', '日本', '科幻',
                '悬疑', '恐怖']


def get_html(my_url):
    """
    获得网页的html
    :param my_url: 网页链接
    :return:
    """
    page = urllib.urlopen(my_url)
    my_html = page.read()
    return my_html

for k in range(14):
    for i in range(10):
        douban_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=' \
                   + urllib.quote(douban_class[3]) + \
                   '&sort=recommend&page_limit=20&page_start=%s' % (i * 20)
        douban_html = get_html(douban_url)
        douban_json = demjson.decode(douban_html)
        for j in range(20):
            cur.execute('insert into movie(title, class ,url, cover, rate) values (%s, %s, %s, %s, %s)',
                        (douban_json['subjects'][j]['title'].encode('utf-8'), douban_class[k],
                         douban_json['subjects'][j]['url'],
                         douban_json['subjects'][j]['cover'], douban_json['subjects'][j]['rate']))

conn.commit()
cur.close()
conn.close()
