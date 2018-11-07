# -*- coding:utf-8 -*-
import urllib
from urllib import request
from bs4 import BeautifulSoup
import re

def url_search(key):
    count = 0
    for i in range(0,76):
        url = 'http://www.baidu.com/s?wd=' + urllib.parse.quote(key)  + "&rn=100&pn="+str(i*10)  # legal url
        response = request.urlopen(url)
        current_page = response.read()
        soup = BeautifulSoup(current_page, 'lxml')
        # title = soup.find_all('h3',class_='t')
        print('第{}页'.format(i+1))
        for result_table in soup.find_all('h3', class_='t'):
            a_click = result_table.find("a")
            count = count + 1
            row = [count,a_click.get_text()]
            print(row)
            # print(a_click.get_text())  # 标题

            # print(str(a_click.get("href")))  # 链接


if __name__ == '__main__':
    url_search("高莹")