from selenium import webdriver
from lxml import etree
from tqdm import tqdm
import requests
import time
import os



class WyyyySpider(object):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('detach',True)
    driver_path = r'D:\ChromeDriver\chromedriver.exe'
    def __init__(self,song_name):
        self.driver = webdriver.Chrome(executable_path=self.driver_path,options=self.option)
        self.song = song_name
        self.url = f'https://music.163.com/#/search/m/?s={self.song}&type=1'
        self.headers = {
            'referer': 'https://music.163.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        }
    def run(self):
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.switch_to.frame('g_iframe')
        source = self.driver.page_source
        self.parse_page(source)


    def parse_page(self,source):
        # pass
        html = etree.HTML(source)
        song_infos = html.xpath("//div[starts-with(@class,'item f-cb h-flag ')]")
        song_link_list = []
        song_name_list = []
        song_singer_list=[]
        for song_info in song_infos:
            song_link = song_info.xpath(".//div[@class='sn']//div[@class='text']/a/@href")[0]
            link = 'https://music.163.com/#'+song_link
            if not 'mv' in link:
                song_link_list.append(link)

            song_name = song_info.xpath(".//div[@class='sn']//div[@class='text']//b/@title")[0]
            song_name_list.append(song_name)

            song_singer = song_info.xpath(".//div[@class='td w1']//div[@class='text']")
            for singer in song_singer:
                singers = singer.xpath(".//a/text()")
                singer = ' '.join(text for text in singers)
                song_singer_list.append(singer)
        self.driver.quit()

        num =1
        songs = {}
        for name,link,singer in zip(song_name_list,song_link_list,song_singer_list):
            print(f'{num}-?????????:{name}"\t"??????:{singer}')
            song_id = link.split('id=')[-1]
            url = f'http://music.163.com/song/media/outer/url?id={song_id}.mp3'
            songs[num] = url
            num += 1

        print('\n')
        user_choice_song = int(input('????????????????????????????????????>>>'))
        download_url = songs[user_choice_song]
        if not os.path.exists('?????????????????????'):
            os.mkdir('?????????????????????')
        song_name = song_name_list[user_choice_song+1]
        with open(f'?????????????????????/{song_name}.mp3','wb')as f:
            f.write(requests.get(download_url,headers = self.headers).content)
        for i in tqdm(range(int(10e6)),ncols=88,desc='??????????????????...'):
            pass


def main():
    song_name = input('?????????????????????????????????>>>')
    spider = WyyyySpider(song_name)
    spider.run()

if __name__ == '__main__':
    main()











# import urllib.parse as parse
# from selenium import webdriver
# import time
# import urllib.request
# import os
# import sys
#
#
# def Time_1():     #  ???????????????
#     for i in range(1,51):
#         sys.stdout.write('\r')
#         sys.stdout.write('{0}% |{1}'.format(int(i%51)*2,int(i%51)*'???'))
#         sys.stdout.flush()
#         time.sleep(0.125)
#     sys.stdout.write('\n')
#
# def Music_search():
#     print('-----------------------?????????----------------------------')
#     url='https://music.163.com/#/search/m/?%s&type=1'%(parse.urlencode({'s':input('????????????????????????')}))
#
#     driver=webdriver.Chrome(executable_path='D:\ChromeDriver\chromedriver.exe')
#     driver.get(url=url)
#     driver.switch_to.frame('g_iframe')
#     page=driver.find_element_by_id('m-search')
#     song_id_list=page.find_elements_by_xpath('.//div[@class="sn"]/div[@class="text"]/a')# ????????????????????????????????????
#     song_name_list=page.find_elements_by_xpath('.//div[@class="sn"]/div[@class="text"]/a/b')
#     song_id_list_1=[] # ?????????????????????
#
#     for i in range(len(song_id_list)):
#         song_id_list[i]=song_id_list[i].get_attribute('href')
#         if 'song'in song_id_list[i]:
#             song_id_list_1.append(song_id_list[i])
#
#
#     for i in range(len(song_name_list)):
#         song_name_list[i]=song_name_list[i].get_attribute('title')
#
#     driver.close()
#     return song_name_list,song_id_list_1 # ???????????????????????????id
#
# def Downlad(music_name,url_1):
#     id=url_1[url_1.find('id='):]
#     url='https://music.163.com/song/media/outer/url?{}.mp3'.format(id)
#     try:
#         os.mkdir(path='./???????????????')
#     except Exception as e:
#         print(e,'??????????????????????????????????????????')
#     finally:
#         print('{}.mp3????????????????????????????????????...'.format(music_name))
#         Time_1()
#         urllib.request.urlretrieve(url=url, filename='./???????????????/{}.mp3'.format(music_name))
#         print('{}.mp3?????????????????????'.format(music_name))
#         print('????????????????????????????????????')
#
# if __name__ == '__main__':
#     list_1=Music_search()
#     print('??????????????????????????????')
#     for i in range(len(list_1[0])):
#         print('-{}-{}'.format(i+1,list_1[0][i]))
#     i=int(input('???????????????????????????????????????'))
#     Downlad(list_1[0][i-1],list_1[1][i-1])
