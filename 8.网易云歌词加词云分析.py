from selenium import webdriver
from lxml import etree
import time
from pyecharts.charts import WordCloud
from pyecharts.globals import ThemeType
import pyecharts.options as opts
import pandas as pd
import jieba


FILTER_WORDS = ['知道','影评', '电影', '影片', '这么', '那么', '怎么', '如果', '是','喎',
                '\n','的', '一部','这部', '这个', '一个', '这种', '时候', '什么', '没有',
                '还有','这样','...','那样','the','一直','我','你','其实','觉得', '不过',
                '他们','那个','片子','为了','以为','继续','。','一些','其实','时候','认为',
                '可能','今天','不会','一样','个人','因为','所以','一次','看过','非常','么',
                '虽然','但是','评论','还是','需要','整体','观众','自己','最后','有点','很多'
                ,'感觉','这些','一点','一下','一种','作为','问题','不能','看到','东西','比如']

class WyyyyLyricSpider(object):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach',True)
    driver_path = r'D:\ChromeDriver\chromedriver.exe'

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path,options = self.options)
        self.url = 'https://music.163.com/#/song?id=26305541'

    def run(self):
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.switch_to.frame('g_iframe')
        source = self.driver.page_source
        self.crawl_data(source)

    def crawl_data(self,source):
        html = etree.HTML(source)
        lyrics = html.xpath("//div[@id='lyric-content']/text() | //div[@id='flag_more']/text()")
        self.driver.quit()
        contents = ''
        for lyric in lyrics:
            contents += lyric +'\n'
        self.analyse_data(contents)

    def analyse_data(self,contents):
        jieba_list = list(jieba.cut(contents))
        keyword_counts = pd.Series(jieba_list)
        keyword_counts = keyword_counts[keyword_counts.str.len() >= 2]
        keyword_counts = keyword_counts[~keyword_counts.str.contains('|'.join(FILTER_WORDS))]
        keyword_counts = keyword_counts.value_counts()[:80]

        wordcloud = WordCloud(init_opts=opts.InitOpts(theme=ThemeType.ROMANTIC, width='888px', height='666px'))
        wordcloud.set_global_opts(title_opts=opts.TitleOpts(title='小酒窝词云图'))
        data = tuple(zip(keyword_counts.index.tolist(), keyword_counts.tolist()))
        wordcloud.add('', data, word_size_range=[20, 100], shape='diamond')
        print('“"小酒窝"词云图生成中')
        wordcloud.render('小酒窝词云图.html')



def main():
    spider = WyyyyLyricSpider()
    spider.run()

if __name__ == '__main__':
    main()