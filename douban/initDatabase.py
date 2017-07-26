# coding: utf-8
# author: Zhengpeng Xiang
# date: 2016/10/02

import MySQLdb


def create(cur_):
    cur_.execute('create table movie'
                 '(title VARCHAR (100) NOT NULL,'
                 'class VARCHAR(100) NOT NULL,'
                 'url VARCHAR (200) NOT NULL ,'
                 'cover VARCHAR (200) NOT NULL,'
                 'rate VARCHAR(10) NOT NULL);'
                 )

conn = MySQLdb.connect(host='localhost', user='root', passwd='', port=3306)
cur = conn.cursor()
conn.select_db('douban')
# # create(cur)
# #
# cur.execute('select * from movie;')
# for item in cur.fetchall():
#     print item[0], item[1]
