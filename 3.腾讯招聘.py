from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time
import csv


class TencentCareerSpider(object):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach',True)
    driver_path = r'D:\ChromeDriver\chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path,options=self.options)
        self.url = 'https://careers.tencent.com/search.html?query=ot_40006&index=15'
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            self.parse_page(source)
            time.sleep(2)
            WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_element_located((By.XPATH,"//li[@class='next']"))
            )
            nextBtn = self.driver.find_element_by_xpath("//li[@class='next']")
            self.driver.execute_script("arguments[0].scrollIntoView();",nextBtn)  #滚动到某个元素位置
            time.sleep(1)
            nextBtn.click()
            if 'next disabled' in nextBtn.get_attribute('class'):
                source = self.driver.page_source
                self.parse_page(source)
                break
        self.driver.quit()

    def parse_page(self,source):
        html = etree.HTML(source)
        WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,"//a[@class='recruit-list-link']/h4"))
        )
        titles = html.xpath("//a[@class='recruit-list-link']/h4/text()")
        locations = html.xpath("//p[@class='recruit-tips']/span[2]/text()")
        pubtimes = html.xpath("//p[@class='recruit-tips']/span[4]/text()")
        responsibilitys = html.xpath("//p[@class='recruit-text']/text()")
        for title,location,pubtime,responsibility in zip(titles,locations,pubtimes,responsibilitys):
            data = (title,location,pubtime,responsibility)
            self.storage_data(data)
    def storage_data(self,data):
        with open('TencentCareer.csv','a',encoding='utf8',newline='')as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerow(data)
            print('存储了一条职位信息...')

def main():
    csvfile_head = ['title','location','pubtime','responsibility']
    with open('TencentCareer.csv', 'a', encoding='utf8', newline='') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(csvfile_head)
    spider = TencentCareerSpider()
    spider.run()

if __name__ == '__main__':
    main()