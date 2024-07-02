import os
import ctypes

from flask import Flask, request, jsonify
from ctypes import *

app = Flask(__name__)

@app.route('/')
def hello():
    return '欢迎使用微信云托管========！';

@app.route('/getData', methods=['GET'])
def getData():
    data = {"name":"xiaoming", "age":"18"}
    return data;

@app.route('/add', methods=['POST'])
#def add(a, b):
#    return a+b;
def add():
    a1 = request.json['a'];
    b1 = request.json['b'];
    sum = a1+b1;
    return sum;

@app.route('/search', methods=['POST'])
def search():
    keyword = request.json['keyword']
    return jsonify(keyword);

##########################################################


@app.route('/cb_sayhello')
def cb_sayhello():						# 无参数的回调函数
  
    solib =  ctypes.CDLL('./libhello.so')   # 加载动态链接库
    
    func_send_message = solib.send_message
    # CFUNCTYPE定义方法的签名，第一参数表示方法的返回类型，后面开始编译参数的类型
    funcStruct =  CFUNCTYPE(None)			
    solib.send_message(10,funcStruct(cb_sayhello))
    print("============================")
    
    return "hello world";

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
