import time
import csv
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class WxappSpider(object):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach',True)
    driver_path = r'D:/ChromeDriver/chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = self.driver_path,options = self.options)
        self.url = 'https://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1'

    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            self.parse_page(source)
            WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.XPATH,"//a[@class='nxt']"))
            )
            next_btn = self.driver.find_element_by_xpath("//a[@class='nxt']")
            if not next_btn:
                self.driver.quit()
                break
            self.driver.execute_script('arguments[0].scrollIntoView();',next_btn)
            next_btn.click()
            time.sleep(2)

    def parse_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//h3[@class='list_title']/a/@href")
        for link in links:
            self.parse_detail_url(link)
            time.sleep(1)

    def parse_detail_url(self,link):
        self.driver.execute_script('window.open("{}")'.format(link))
        self.driver.switch_to.window(self.driver.window_handles[1])
        source = self.driver.page_source
        WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.XPATH,"//td[@id='article_content']"))
        )
        self.crawl_data(source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def crawl_data(self,source):
        html = etree.HTML(source)
        title = html.xpath("//h1[@class='ph']/text()")[0].strip()
        author = html.xpath("//p[@class='authors']/a/text()")[0].strip()
        pub_time = html.xpath("//p[@class='authors']/span/text()")[0].strip()
        articles = html.xpath("//td[@id='article_content']//text()")
        article = ''.join(text.strip().replace('\r','').replace('\n','') for text in articles)
        data = [title,author,pub_time,article]
        self.storage_data(data)

    def storage_data(self,data):
        with open('wxapp_course.csv', 'a', encoding='utf8', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerow(data)


def main():
    csv_head = ['title','author','pub_time','article']
    with open('wxapp_course.csv','a',encoding = 'utf8',newline='')as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(csv_head)
    spider = WxappSpider()
    spider.run()

if __name__ == '__main__':
    main()