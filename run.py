import os
import ctypes

from flask import Flask, request, jsonify
from ctypes import *

app = Flask(__name__)

def loc_get_size(index):
    s_mark = [
        3, 5, 7, 9, 11, 27, 33, 37, 63
    ]
    return s_mark[index] * s_mark[index]

def cv_rect_to_c_int_ptr(rect):
    # 将 Python 元组 (x, y, width, height) 转换为 ctypes 指针
    rect_array = (ctypes.c_int * 4)(*rect)
    return ctypes.cast(rect_array, ctypes.POINTER(ctypes.c_int))

def output_txt(file, data):
    try:
        with open(file, 'w') as f:
            f.write("{:<10} {:<15} {:<15}\n".format("Pos", "X", "Y"))
            for k in range(0, len(data), 2):
                x = data[k] if k < len(data) else 0
                y = data[k+1] if (k+1) < len(data) else 0
                f.write("{:<10} {:<15} {:<15}\n".format((k//2)+1, x, y))
        return True
    except IOError:
        return False

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
    try:
        lib = ctypes.CDLL('./libgalvanometer_correction.so')
        print("Library loaded successfully")
    except OSError as e:
        print(f"Failed to load library: {e}")
        
    image_path = './camera_calibration.jpg'
    is_circle = True
    index = 7
    area = 5
    ls_circle = 0.1
    ls_convex = 0.1
    ls_ineria = 0.1
    ls_kernel = 3
    ls_kernel_cross = 7
    ls_area_max = 500000
    ls_area_min = 1
    rect_instance = (0, 0, 1080, 985)  

    func_camera_calibration = lib.camera_calibration
    success = func_camera_calibration(
        image_path.encode('utf-8'),
        cv_rect_to_c_int_ptr(rect_instance),
        ctypes.c_bool(is_circle),
        ctypes.c_int(index),
        ctypes.c_double(area),
        ctypes.c_double(ls_circle),
        ctypes.c_double(ls_convex),
        ctypes.c_double(ls_ineria),
        ctypes.c_int(ls_kernel),
        ctypes.c_int(ls_kernel_cross),
        ctypes.c_int(ls_area_max),
        ctypes.c_int(ls_area_min));
    if success:
        return 'Camera calibration successful'
    else
        return 'Camera calibration failed'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
