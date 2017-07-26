# coding: utf-8
# author: Zhengpeng Xiang
# date: 2017/07/26

import requests
from bs4 import BeautifulSoup as bs


class Spider:
    def __init__(self, keywords, number_of_results):
        """
        :param keywords: 搜索的关键词
        :param number_of_results: 搜索的结果数量
        """
        # 基本属性
        self.text = []  # 爬取结果
        self.html = []  # 每一次爬取到的页面
        self.keywords = keywords  # 搜索的关键词
        self.number_of_results = number_of_results  # 指定搜索结果的数量
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0 cb) like Gecko'}  # 请求Header
        self.number_of_pages_stored = 0  # 已经爬取过的页数
        print self.number_of_pages_stored
        # 运行
        self.run()

    def get_html(self, number_of_pages):
        """
        from https://github.com/fancoo/BaiduCrawler/blob/master/baidu_crawler.py
        :return:
        """
        html_ = []

        # 抓取数据内容
        for i in xrange(number_of_pages):
            key = {'wd': self.keywords, 'pn': (i + self.number_of_pages_stored) * 10}
            web_content = requests.get("https://www.baidu.com/s?", params=key, headers=self.headers, timeout=4)
            print web_content.url
            html_.append(web_content.text)

        return html_

    def html_parser(self):
        """
        解析html
        """
        text_ = []
        for i in xrange(len(self.html)):
            soup = bs(self.html[i], 'lxml').find('div', id="content_left")

            # 找到所有class为c-abstract的div
            # 分析了一下，只有这个标签中的数据是我们需要的文本
            # 然后可以再去爬一下百度百科
            c_abstract = soup.find_all('div', class_="c-abstract")

            # 提取数据
            if len(c_abstract) != 0:
                for item_ in c_abstract:
                    text_.append(item_.text.strip())
        return text_

    def run(self, number_of_pages_stored_=None, text_=None, html_=None, number_of_results_=None, keywords_=None):
        """
        爬取指定数目的百度搜索结果
        """
        if number_of_pages_stored_ is not None or text_ is not None or html_ is not None or \
           number_of_results_ is not None or keywords_ is not None:
            # 设置参数
            self.set(number_of_pages_stored_=number_of_pages_stored_, text_=text_, html_=html_,
                     number_of_results_=number_of_results_, keywords_=keywords_)

        # 爬取百度的搜索结果
        while len(self.text) < self.number_of_results:
            # 计算需要抓取的页面的数量
            number_of_pages = (self.number_of_results - len(self.text)) / 10
            self.html = self.get_html(number_of_pages)
            self.text.extend(self.html_parser())
            self.number_of_pages_stored += number_of_pages

        print "从百度搜索结果中共爬取%s个结果，爬取完成！" % self.number_of_results

    def set(self, number_of_pages_stored_=None, text_=None, html_=None, number_of_results_=None, keywords_=None):
        """
        设置类中的属性值
        """
        if number_of_pages_stored_ is not None:
            self.number_of_pages_stored = number_of_pages_stored_

        if text_ is not None:
            self.text = text_

        if html_ is not None:
            self.html = html_

        if number_of_results_ is not None:
            self.number_of_results = number_of_results_

        if keywords_ is not None:
            self.keywords = keywords_
        print "设置参数完毕！"

    def get_result(self):
        """
        输出爬取得结果
        :return:
        """
        return self.text

if __name__ == '__main__':
    s = Spider
    text = s('游戏名字', 20).get_result()
    for item in text:
        print item

    print '******************'

    text = s('游戏名字', 10).get_result()
    for item in text:
        print item
