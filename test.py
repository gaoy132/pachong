import pymysql
import configparser     #connect configuration file
import csv
import xlwt
import codecs
from DBUtils.PooledDB import PooledDB

def export_excel(c):
    cf = configparser.ConfigParser()
    cf.read("sqlconfig.conf")
    host = cf.get("db", "host")
    user = cf.get("db", "user")
    password = cf.get("db", "password")
    db_name = cf.get("db", "database")
    port = cf.get("db", "port")
    pool = PooledDB(pymysql, 10, host=host, user=user, password=password, db=db_name, port=int(port))
    con = pool.connection()
    cursor = con.cursor()
    sql = 'select * from %s' % c  # get table's name
    cursor.execute(sql)
    fileds = [filed[0] for filed in cursor.description]
    all_data = cursor.fetchall()  # all data
    # 写excel
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # create a book
    sheet = book.add_sheet('sheet1')  # create a sheet


    # col = 0
    # for field in fileds:
    #     sheet.write(0, col, field)
    #     col += 1               # enumerate
    for col, field in enumerate(fileds):  #write tablename
        sheet.write(0, col, field)

        row = 1
    for data in all_data:  # control row
        for col, field in enumerate(data):  # control col
            sheet.write(row, col, field)
        row += 1
    book.save('D:/gy/vm1/baidu.xls')

    with codecs.open('baidu.csv', 'w', 'utf-8') as out:
        csv_write = csv.writer(out, dialect='excel')
        csv_Header = ["num", "title"]
        csv_write.writerow(csv_Header)
        for data in all_data:
            csv_write.writerow(data)
        out.close()

# if __name__ == '__main__':
#     export_excel("高莹最棒")