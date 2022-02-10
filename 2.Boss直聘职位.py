import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import re
import time

class BossSpider(object):
    options = webdriver.ChromeOptions()
    # options.add_argument('--proxy-server=http://221.203.5.232:7376')
    options.add_experimental_option('detach',True)
    driver_path = r'D:\ChromeDriver\chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path,options=self.options)
        self.url = 'https://www.zhipin.com/job_detail/?query=python%E5%85%A8%E6%A0%88%E5%B7%A5%E7%A8%8B%E5%B8%88&city=100010000&industry=&position='
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            self.parse_page(source)
            WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_element_located((By.XPATH,"//a[@class='next']"))
            )
            nextBtn = self.driver.find_element_by_xpath("//a[@class='next']")
            if 'next disabled' in nextBtn.get_attribute('class'):
                break
            else:
                nextBtn.click()
            time.sleep(2)
    def parse_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//span[@class='job-name']/a/@href")
        for link in links:
            self.parse_detail_url(link)
            time.sleep(1.5)
    def parse_detail_url(self,link):
        self.driver.execute_script(f'window.open("{link}")')
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(1)
        source = self.driver.page_source
        WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='name']/h1"))
        )
        self.crawl_data(source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    def crawl_data(self,source):
        html = etree.HTML(source)
        job_name = html.xpath("//div[@class='name']/h1/text()")[0].strip()
        job_salary = html.xpath("//div[@class='name']/span")
        job_salary = job_salary[0].xpath(".//text()")[0].strip()
        job_loca = html.xpath("//a[@class='text-city']/text()")[0].strip()
        education = html.xpath("//div[@class='info-primary']/p/text()")
        job_exepreience = education[0].strip()
        job_need_edu = education[1].strip()
        job_responsibility = html.xpath("//div[@class='text']//text()")
        job_responsibility = ''.join(text.strip().replace(' ','') for text in job_responsibility)
        result = [job_name,job_salary,job_loca,job_exepreience,job_need_edu,job_responsibility]
        with open('Boss直聘.csv', 'a', encoding='utf8', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerow(result)
            print('存储了一条职位信息。。。')
    def storage_data(self):
        pass

def main():
    csvfile_head = ['工作名称','薪资','地点','经验','学历','工作职责']
    with open('Boss直聘.csv','a',encoding='utf8',newline='')as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(csvfile_head)
    spider = BossSpider()
    spider.run()

if __name__ == '__main__':
    main()