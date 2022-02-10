from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time
import csv

class DoubanMovieTop250Spider(object):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach',True)
    driver_path = r'D:\ChromeDriver\chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path,options=self.options)
        self.url = 'https://movie.douban.com/top250?start=0&filter='
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            self.parse_page(source)
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='paginator']/span[3]/a"))
            )
            nextPageBtn = self.driver.find_element_by_xpath("//div[@class='paginator']/span[3]/a")
            self.driver.execute_script("arguments[0].scrollIntoView();",nextPageBtn )
            time.sleep(1)
            nextPageBtn.click()
            time.sleep(1)
    def parse_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//div[@class='info']//a/@href")
        for link in links:
            self.parse_detail_url(link)
            time.sleep(1)
    def parse_detail_url(self,link):
        self.driver.execute_script('window.open("{}")'.format(link))
        self.driver.switch_to.window(self.driver.window_handles[1])
        source = self.driver.page_source
        self.crawl_data(source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    def crawl_data(self,source):
        html = etree.HTML(source)
        try:
            movie_title_infos = html.xpath("//div[@id='content']//h1/span/text()")
            movie_title = movie_title_infos[0].strip()
            movie_year = movie_title_infos[1].strip()
            movie_director = html.xpath("//div[@id='info']/span[1]/span[@class='attrs']/a/text()")[0].strip()
            movie_main_actor = html.xpath("//div[@id='info']/span[3]/span[@class='attrs']/span[1]/a/text()")[0].strip()
            movie_spans= html.xpath("//div[@id='info']/span[5]/text() | //div[@id='info']/span[6]/text()")
            movie_type = ','.join(type.strip() for type in movie_spans)
            movie_score = html.xpath("//strong[@class='ll rating_num']/text()")[0]
            movie_coment_people = html.xpath("//span[@property='v:votes']/text()")[0]
            movie_info = [movie_title,movie_year,movie_director,movie_main_actor,movie_score,movie_coment_people,movie_type]
            self.storage_data(movie_info)
        except:
            pass
    def storage_data(self,data):
        with open('douban_movie_top_250.csv','a',encoding='utf8',newline='')as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerow(data)
            print('存储了一个电影信息。。。')

def main():
    csvfile_head = ['电影名称','年份','导演','主演','评分','评价人数','类型']
    with open('douban_movie_top_250.csv', 'a', encoding='utf8', newline='') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(csvfile_head)
    spider = DoubanMovieTop250Spider()
    spider.run()

if __name__ == '__main__':
    main()