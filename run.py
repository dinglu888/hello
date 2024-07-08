import os
import ctypes
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

from flask import Flask, request, jsonify, json
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
    try:
        lib = ctypes.CDLL('./libgalvanometer_correction.so')
        #return 'Library loaded successfully'
    except OSError as e:
        return f'Failed to load library:{e}'
        
        
    # 定义 camera_calibration 和 galvanometer_correction 函数的参数和返回类型
    lib.camera_calibration.argtypes = [
        ctypes.c_char_p,  # const char* (as img_path)
        ctypes.POINTER(ctypes.c_int),  # int* (as rect array)
        ctypes.c_bool,  # bool (is_circle)
        ctypes.c_int,  # int (index)
        ctypes.c_double,  # double (area)
        ctypes.c_double,  # double (ls_circle)
        ctypes.c_double,  # double (ls_convex)
        ctypes.c_double,  # double (ls_ineria)
        ctypes.c_int,  # int (ls_kernel)
        ctypes.c_int,  # int (ls_kernel_cross)
        ctypes.c_int,  # int (ls_area_max)
        ctypes.c_int   # int (ls_area_min)
    ]
    lib.camera_calibration.restype = ctypes.c_bool
     
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
