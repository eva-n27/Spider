# coding: utf-8
# author: Zhengpeng Xiang
# date: 2017/07/26


import requests
from bs4 import BeautifulSoup as bs


class Spider:
    """
    function:
        - 爬虫类，用于将爬取百度搜索的结果爬取下来。
        - 给Spider的实例s使用run()方法传入keywords, number_of_results之后就可以自动爬取，使用get_result()方法获得爬取得结果
        - 使用run方法重复使用实例s，可传递（number_of_results, keywords）等参数
    input:
        - 使用run()方法进行传递
        - keywords 搜索的关键词，字符串
        - number_of_results 搜索的结果数，整数
    output:
        - text 使用get_result方法获得,一维list，每一个元素对应一个搜索结果中的文本
    """
    def __init__(self):
        # 输入
        self.keywords = ''  # 搜索的关键词
        self.number_of_results = 0  # 指定搜索结果的数量

        # 基本属性
        self.text = []  # 爬取结果
        self.html = []  # 每一次爬取到的页面
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0 cb) like Gecko'}  # 请求Header
        self.number_of_pages_stored = 0  # 已经爬取过的页数

    def get_html(self, number_of_pages):
        """
        爬取html
        """
        html = []

        # 抓取数据内容
        for i in xrange(number_of_pages):
            key = {'wd': self.keywords, 'pn': (i + self.number_of_pages_stored) * 10}  # pn表示页数
            web_content = requests.get("https://www.baidu.com/s?", params=key, headers=self.headers, timeout=4)
            print web_content.url
            html.append(web_content.text)

        print "html下载完成！"
        return html

    def html_parser(self):
        """
        解析html
        """
        text = []
        for i in xrange(len(self.html)):
            soup = bs(self.html[i], 'lxml').find('div', id="content_left")

            # 找到所有class为c-abstract的div
            # 分析了一下，只有这个标签中的数据是我们需要的文本
            # 然后可以再去爬一下百度百科
            c_abstract = soup.find_all('div', class_="c-abstract")

            # 提取数据
            if len(c_abstract) != 0:
                for item_ in c_abstract:
                    text.append(item_.text.strip())
        print "html解析完成！"
        return text

    def run(self, keywords, number_of_results):
        """
        爬取指定数目的百度搜索结果
        """
        self.clean()

        self.keywords = keywords
        self.number_of_results = number_of_results

        # 爬取百度的搜索结果
        while len(self.text) < self.number_of_results:
            # 计算需要抓取的页面的数量
            if self.number_of_results - len(self.text) >= 10:
                number_of_pages = (self.number_of_results - len(self.text)) / 10
            else:
                number_of_pages = 1

            self.html = self.get_html(number_of_pages)

            # 保存爬取得结果，仅保留number_of_results个结果
            result_text = self.html_parser()
            if len(result_text + self.text) > self.number_of_results:
                self.text.extend(result_text[:self.number_of_results - len(self.text)])
            else:
                self.text.extend(result_text)

            self.number_of_pages_stored += number_of_pages

        print "从百度搜索结果中共爬取%s个结果，爬取完成！" % self.number_of_results
        return self

    def clean(self):
        """
        将类中的属性值清空
        """
        self.text = []
        self.html = []
        self.number_of_pages_stored = 0

        print "参数清空完毕！"
        return self

    def get_result(self):
        """
        输出爬取得结果
        :return:
        """
        return self.text


if __name__ == '__main__':
    s = Spider()
    text = s.run('游戏名字', 20).get_result()
    for item in text:
        print item

    print '******************'

    text = s.run(keywords='游戏名字', number_of_results=10).get_result()
    for item in text:
        print item
