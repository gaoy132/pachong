# -*- coding:utf-8 -*-
import urllib
from urllib import request
from bs4 import BeautifulSoup
import re



def getresultcount(word):
    url = 'http://www.baidu.com/s?wd=' + urllib.parse.quote(word)       #legal url
    response = request.urlopen(url)
    current_page = response.read()
    soup = BeautifulSoup(current_page, 'lxml')
    # for x in soup.find_all('span', string=re.compile('百度为您找到相关结果')):
    #     result = re.sub(r"\D", "", x.renderContents().decode("utf-8"))    #regular expression.substitude
    #     # print('results count:  '+str(result))
    #     return result
    x = soup.find_all('span', string=re.compile('百度为您找到相关结果'))
    print(str(x))
    return str(x)
