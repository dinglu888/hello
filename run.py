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
    lib = ctypes.CDLL('./libgalvanometer_correction.so')
    func_camera_calibration = lib.camera_calibration  

    return '111111'    
        
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
    
    return '22222'
    
    rect_instance = (0, 0, 1080, 985) 
    rect_array = (ctypes.c_int * 4)(*rect_instance)
    
    return '33333'

    success = func_camera_calibration(
        image_path.encode('utf-8'),
        ctypes.cast(rect_array, ctypes.POINTER(ctypes.c_int)),
        ctypes.c_bool(is_circle),
        ctypes.c_int(index),
        ctypes.c_double(area),
        ctypes.c_double(ls_circle),
        ctypes.c_double(ls_convex),
        ctypes.c_double(ls_ineria),
        ctypes.c_int(ls_kernel),
        ctypes.c_int(ls_kernel_cross),
        ctypes.c_int(ls_area_max),
        ctypes.c_int(ls_area_min)
    )
    
    if success:
        return 'Camera calibration successful'
    else:
        return 'Camera calibration failed'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
