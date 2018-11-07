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

    with codecs.open('Stu_csv.csv', 'w', 'utf-8') as out:
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

    def save_to_DB(form_name,num,title1):
        # con = pymysql.connect(host=host, user=user, password=password, db=db_name, port=int(port))
        # pool = PooledDB(pymysql, 10, host=host, user=user, password=password, db=db_name, port=int(port))
        con = pool.connection()
        cursor = con.cursor()
        sql = "INSERT INTO {} VALUES('{}','{}')".format(form_name,num,title1) # implement sql
        try:
            cursor.execute(sql)
            con.commit()# implement in db
            print("数据存入成功")
        except Exception as e:
            print(e)
            con.rollback()  # if error
        finally:
            con.close()


    def get_cont(key):
        driver.find_element_by_id('kw').send_keys(key)  # search line,input "key"
        driver.find_element_by_id('su').click()  # search key
        wait = WebDriverWait(driver, 10)
        # wait.until(EC.presence_of_element_located((By.ID, 'foot')))
        # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#kw')))
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '下一页>')))
        cont = driver.find_element_by_class_name('nums_text')
        print(cont.text)

    def search(key):
        get_cont(key)
        i = 0  # cont
        while True:
            # content_h3_a = driver.find_elements_by_xpath('//*[@class="t"]/a')    #find title from "a"
            content_h3_a = driver.find_elements_by_xpath('//*/h3')
            for title in content_h3_a:
                i = i + 1
                save_to_DB(key,i, title.text)
                row = [i, title.text]
                print(row)
                # csv
                try:
                    with codecs.open('Stu_csv.csv', 'a', 'utf-8') as out:
                        csv_write = csv.writer(out, dialect='excel')
                        csv_write.writerow(row)
                except:
                    print("csv存入失败")
                # excel
                try:
                    for j in range(0, len(row)):
                        sheet.write(i, j, row[j])
                except:
                    print("excel存入失败")
            out.close()
            book.save('D:/gy/vm1/hh.xls')
            try:
                currentpage = driver.find_element_by_link_text('下一页>')  # currentpage's
                currentpage.click()
                nextpage = driver.find_element_by_link_text('下一页>')  # nextpage's
                while (currentpage == nextpage):  # if currentpage=nextpage,not load nextpage
                    # wait until nextpage!=currentpage,already load nextpage
                    nextpage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, '下一页>')))
            except:
                 content_h3_a = driver.find_elements_by_xpath('//*/h3')
                 for title in content_h3_a:
                     i = i + 1
                     save_to_DB(i, title.text)
                     row = [i, title.text]
                     print(row)
                     # csv
                     try:
                         with codecs.open('Stu_csv.csv', 'a', 'utf-8') as out:
                             csv_write = csv.writer(out, dialect='excel')
                             csv_write.writerow(row)
                     except:
                         print("csv存入失败")
                     # excel
                     try:
                         for j in range(0, len(row)):
                             sheet.write(i, j, row[j])
                     except:
                         print("excel存入失败")

                 out.close()
                 book.save('D:/gy/vm1/hh.xls')
                 print('THE END')
                 break


    con_init(a)

    # driver = webdriver.Chrome()
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=op)
    driver.get('http://www.baidu.com')
    search(a)
    # return a
    # export_excel(aa)
if __name__ == '__main__':
    baidu_search("hello")

