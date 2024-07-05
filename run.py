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
    
@app.route('/cb_sayhello')
def cb_sayhello(): 
    solib =  ctypes.CDLL('./libhello.so')   # 加载动态链接库  
    func_say_hello4 = solib.say_hello4
    res = func_say_hello4(1,2);  
    return jsonify(res);


##########################################################
   
@app.route('/camera_calibration', methods=['POST'])
def camera_calibration():
    index = request.json['index'];
    area = request.json['area'];
    ls_circle = request.json['ls_circle'];
    name = request.json['name'];
    
    json_str = '{"name": "John", "age": 30, "age1": 20, "city": "New York"}'
    data = json.loads(json_str)
    age = data["age"]
    age1 = data["age1"]
    
    solib =  ctypes.CDLL('./libhello.so')   # 加载动态链接库  
    func_say_hello4 = solib.say_hello4
    res = func_say_hello4(age,age1);  
    return jsonify(res);
    
    #str = "%s,%s,%s,%s" %(index, area, ls_circle, name)
    #return str;

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
