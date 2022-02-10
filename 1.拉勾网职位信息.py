from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
import time
import re

class LagouSpider(object):
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True) #防止网页自动退出
    driver_path = r'D:\ChromeDriver\chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = self.driver_path,options=self.option)
        self.url = 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
    def run(self):
        self.driver.get(self.url)
        while True:
            # 通过模拟浏览器获得的源代码，是包含ajax数据的！！！！
            source = self.driver.page_source
            WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_element_located((By.XPATH,"//div[@class='pager_container']/span[last()]"))
            )
            self.parse_page(source)
            nextBtn = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
            if 'pager_next pager_next_disabled' in nextBtn.get_attribute('class'):
                break
            else:
                nextBtn.click()
                print(self.driver.current_url)

    def parse_page(self,source):
        html = etree.HTML(source)
        position_links = html.xpath("//a[@class='position_link']/@href")
        for position_link in position_links:
            self.parse_detail_url(position_link)
            time.sleep(1.5)

    def parse_detail_url(self,link):
        # self.driver.get(link)
        self.driver.execute_script('window.open("{}")'.format(link))
        self.driver.switch_to.window(self.driver.window_handles[1])
        source = self.driver.page_source
        #不能查找text()
        WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,"//span[@class='position-head-wrap-position-name']"))
        )
        self.crawl_data(source)
        #关闭当前详情页
        self.driver.close()
        #切换回列表页
        self.driver.switch_to.window(self.driver.window_handles[0])

    def crawl_data(self,source):
        html = etree.HTML(source)
        title = html.xpath("//span[@class='position-head-wrap-position-name']/text()")[0]
        company = html.xpath("//em[@class='fl-cn']/text()")[0].strip()
        salary = html.xpath("//span[@class='salary']/text()")[0].strip()
        position_spans = html.xpath("//dd[@class='job_request']//span")
        location = position_spans[0].xpath(".//text()")[0].strip()
        location = re.sub(r'[\s/]','',location)
        exeprience = position_spans[1].xpath(".//text()")[0].strip()
        exeprience = re.sub(r'[\s/]','',exeprience)
        edu_bg = position_spans[2].xpath(".//text()")[0].strip()
        edu_bg = re.sub(r'[\s/]', '', edu_bg)
        job_detail = html.xpath("//div[@class='job-detail']//text()")
        job_detail = ''.join(text.strip().replace(' ','') for text in job_detail)
        result = {
            'title':title,'company':company,'salary':salary,'location':location,
            'exeprience':exeprience,'edu_bg':edu_bg,'job_tetail':job_detail
        }
        print(result)
    def storage_data(self,result):
        pass

def main():
    spider = LagouSpider()
    spider.run()

if __name__ == '__main__':
    main()