from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time
import csv

class DyttSpider(object):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach',True)
    driver_path = r'D:\ChromeDriver\chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path,options=self.options)
        self.url = 'https://dytt8.net/html/gndy/dyzz/index.html'
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            self.parse_page(source)
            time.sleep(1)
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='co_content8']/div/a[last()-1]"))
            )
            nextBtn = self.driver.find_element_by_xpath("//div[@class='co_content8']/div/a[last()-1]")
            self.driver.execute_script("arguments[0].scrollIntoView();",nextBtn)
            time.sleep(1)
            nextBtn.click()

    def parse_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//td[@height='26']//a/@href")
        for link in links:
            self.parse_detail_url(link)
            time.sleep(1)
    def parse_detail_url(self,link):
        self.driver.execute_script(f'window.open("{link}")')
        self.driver.switch_to.window(self.driver.window_handles[1])
        source = self.driver.page_source
        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='title_all']/h1/font[@color='#07519a']"))
        )
        self.crawl_data(link,source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    def crawl_data(self,link,source):
        html = etree.HTML(source)
        movie_lists = []
        movie = {}
        movie['movie_detail_link'] = link
        movie_name = html.xpath("//div[@class='title_all']/h1/font[@color='#07519a']/text()")[0]
        movie['movie_name'] = movie_name
        movie_poster = html.xpath("//div[@id='Zoom']//img/@src")[0]
        movie['movie_poster'] = movie_poster
        movie_info = html.xpath("//div[@id='Zoom']//text()")
        # print(movie_info)
        for index, info in enumerate(movie_info):
            if info.startswith('???????????????'):
                info = info.replace('??????????????????', '')
                movie['movie_year'] = info
            elif info.startswith('???????????????'):
                info = info.replace('??????????????????', '')
                movie['movie_origin_place'] = info
            elif info.startswith('???????????????'):
                info = info.replace('??????????????????', '')
                movie['movie_type'] = info
            elif info.startswith('???????????????'):
                info = info.replace('??????????????????', '')
                movie['movie_pub_time'] = info
            elif info.startswith('???????????????'):
                info = info.replace('??????????????????', '')
                movie['movie_score'] = info
            elif info.startswith('???????????????'):
                info = info.replace('??????????????????', '')
                movie['movie_director'] = info
            elif info.startswith('???????????????') or info.startswith('????????????  '):
                info = info.replace('??????????????????', '').replace('????????????  ???', '')
                actors = [info]
                for i in range(index + 1, len(movie_info)):
                    actor = movie_info[i].strip()
                    if actor.startswith('???????????????'):
                        break
                    actors.append(actor)
                movie['movie_actors'] = actors
            movie_lists.append(movie)
        print(movie_lists)
    def storage_data(self):
        pass

def main():
    spider = DyttSpider()
    spider.run()

if __name__ == '__main__':
    main()