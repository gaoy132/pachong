# !/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium import webdriver
import pymysql
import configparser     #connect configuration file
import csv
import xlwt
import codecs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from DBUtils.PooledDB import PooledDB
import urllib
from urllib import request
from bs4 import BeautifulSoup
import re



def baidu_search(a):
    cf = configparser.ConfigParser()
    cf.read("sqlconfig.conf")
    host = cf.get("db", "host")
    user = cf.get("db", "user")
    password = cf.get("db", "password")
    db_name = cf.get("db", "database")
    port = cf.get("db", "port")
    pool = PooledDB(pymysql, 10, host=host, user=user, password=password, db=db_name, port=int(port))
    # csv
    # out = open('Stu_csv.csv', 'w', newline='')
    # csv_write = csv.writer(out, dialect='excel')
    # csv_Header = ["num", "title"]
    # csv_write.writerow(csv_Header)
    # out.close()
    # csv

    with codecs.open('csv_current.csv', 'w', 'utf-8') as out:
        csv_write = csv.writer(out, dialect='excel')
        csv_Header = ["num", "title"]
        csv_write.writerow(csv_Header)
        out.close()
    # excel
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    #build a sheet，name:mysheet
    sheet = book.add_sheet('search_content', cell_overwrite_ok=True)
    excel_Header = ["num", "title"]
    for k in range(0, len(excel_Header)):
        sheet.write(0, k, excel_Header[k])

    def con_init(form_name):
        try:
            # con = pymysql.connect(host=host, user=user, password=password, db=db_name, port=int(port))  # connect db
            # pool = PooledDB(pymysql,10,host=host, user=user, password=password, db=db_name, port=int(port))
            con = pool.connection()
            cursor = con.cursor()
            cursor.execute("DROP TABLE IF EXISTS {}".format(form_name))
            sql = """CREATE TABLE {}(
                      num  int,
                      title  VARCHAR(500))""" .format(form_name)   # create a table
            cursor.execute(sql)
            con.commit()
            print("数据库连接成功")
        except:
            print("数据库连接失败")
        finally:
            con.close()

    def save_to_DB(form_name,num,title1):
        # con = pymysql.connect(host=host, user=user, password=password, db=db_name, port=int(port))
        # pool = PooledDB(pymysql, 10, host=host, user=user, password=password, db=db_name, port=int(port))
        con = pool.connection()
        cursor = con.cursor()
        sql = "INSERT INTO {} VALUES('{}','{}')".format(form_name,num,title1) # implement sql
        try:
            cursor.execute(sql)
            con.commit()# implement in db
            # print("数据存入成功")
        except Exception as e:
            print(e)
            con.rollback()  # if error
        finally:
            con.close()


    def search(key):
        # get_cont(key)
        def go(key,i,count):
            url = 'http://www.baidu.com/s?wd=' + urllib.parse.quote(key) + "&rn=100&pn=" + str(i * 10)  # legal url
            response = request.urlopen(url)
            current_page = response.read()
            soup = BeautifulSoup(current_page, 'lxml')
            print('第{}页'.format(i + 1))
            for result_table in soup.find_all('h3', class_='t'):
                a_click = result_table.find("a")
                title = a_click.get_text()
                count = count + 1
                row = [count, title]
                save_to_DB(key, count, title)
                print(row)
                    # csv
                try:
                    with codecs.open('csv_current.csv', 'a', 'utf-8') as out:
                        csv_write = csv.writer(out, dialect='excel')
                        csv_write.writerow(row)
                except:
                        print("csv存入失败")
                    # excel
                try:
                    for j in range(0, len(row)):
                        sheet.write(count, j, row[j])
                except:
                    print("excel存入失败")
            out.close()
            book.save('D:/gy/vm1/excel_current.xls')
            while soup.find_all('a',string=re.compile('下一页>')):
                i=i+1
                go(key,i,count)
                break

        i = 0
        count = 0
        go(key, i,count)
        print("THE END")

    con_init(a)
    search(a)

