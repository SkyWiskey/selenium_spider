from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time
import csv


class QsbkSpider(object):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach',True)
    driver_path = r'D:\ChromeDriver\chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = self.driver_path,options=self.options)
        self.url = 'https://www.qiushibaike.com/text/page/1/'
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            self.parse_page(source)
            WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_element_located((By.XPATH,"//span[@class='next']"))
            )
            nextBtn = self.driver.find_element_by_xpath("//span[@class='next']")
            if not nextBtn:
                break
            self.driver.execute_script("arguments[0].scrollIntoView();",nextBtn)
            nextBtn.click()
            time.sleep(2)
    def parse_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//a[@class='contentHerf']/@href")
        for link in links:
            link = 'https://www.qiushibaike.com' + link
            self.parse_detail_url(link)
            time.sleep(0.5)
    def parse_detail_url(self,link):
        self.driver.execute_script('window.open("{}")'.format(link))
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(1)
        source = self.driver.page_source
        self.crawl_data(source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def crawl_data(self,source):
        html = etree.HTML(source)
        title = html.xpath("//h1[@class='article-title']/text()")[0].strip()
        time = html.xpath("//span[@class='stats-time']/text()")[0].strip()
        funny_num = html.xpath("//i[@class='number']/text()")[0].strip()
        articles = html.xpath("//div[@class='content']//text()")
        article = ''.join(text for text in articles).strip().replace('\n','').replace(' ','')
        data = [title,time,funny_num,article]
        print(data)
        self.storage_data(data)
    def storage_data(self,data):
        with open('糗事百科.csv','a',encoding = 'utf8',newline='')as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerow(data)

def main():
    with open('糗事百科.csv','a',encoding = 'utf8',newline='')as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(['title','time','funny_num','article'])
    spider = QsbkSpider()
    spider.run()
if __name__ == '__main__':
    main()