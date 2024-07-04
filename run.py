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
   
@app.route('/camera_calibration')
def camera_calibration():
    is_circle = request.json['is_circle'];
    index = request.json['index'];
    ls_circle = request.json['ls_circle'];
    ls_area_max = request.json['ls_area_max'];
    name = request.json['name'];
    return jsonify(is_circle) + "," + jsonify(index) + "," + jsonify(ls_circle) + "," + jsonify(ls_area_max) + "," + jsonify(name);


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
