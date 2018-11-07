# -*- coding:utf-8 -*-
from flask import Flask,render_template,request,make_response,send_from_directory
# import baidu as baidu
import baidu_1 as baidu_1
import test as test
import title_cont
app = Flask(__name__)


# @app.route('/search',methods=['POST'])
# def get_keyword():
#     if request.method == 'POST':
#         keyword = request.form['keyword']
#     baidu.baidu_search(keyword)
#     return send_from_directory('','hh.xls')

@app.route('/search/<string:keyword>',methods=['GET'])
def get_keyword(keyword):
    # baidu.baidu_search(keyword)
    baidu_1.baidu_search(keyword)
    rst = make_response("搜索完成")
    return rst

@app.route('/count/<string:keyword>',methods=['GET'])
def get_count(keyword):
    rst=make_response(title_cont.getresultcount(keyword))
    # rst = make_response(keyword)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

@app.route('/download/<string:keyword>',methods=['GET','POST'])
def get_excel(keyword):
    try:
        test.export_excel(keyword)
        print("导出excel、csv")
        # return send_from_directory('', 'baidu.xls')
    except Exception as e:
        print(e)

# @app.route('/download/csv/',methods=['get','POST'])
# def get_csv():
#     try:
#         test.export_excel("baidu")
#         print("导出csv")
#         return send_from_directory('', 'baidu.csv')
#     except Exception as e:
#         print(e)


if __name__ == '__main__':
    app.run()

