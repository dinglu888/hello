import os
import ctypes


from flask import Flask, request, jsonify, json
from ctypes import *

app = Flask(__name__)

def cv_rect_to_c_int_ptr(rect):
    # 将 Python 元组 (x, y, width, height) 转换为 ctypes 指针
    rect_array = (ctypes.c_int * 4)(*rect)
    return ctypes.cast(rect_array, ctypes.POINTER(ctypes.c_int))

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

    data = request.json
    is_circle = bool(data['is_circle'])
    index = int(data['index'])
    area = float(data['area'])
    ls_circle = float(data['ls_circle'])
    ls_convex = float(data['ls_convex'])
    ls_ineria = float(data['ls_ineria'])
    ls_kernel = int(data['ls_kernel'])
    ls_kernel_cross = int(data['ls_kernel_cross'])
    ls_area_max = int(data['ls_area_max'])
    ls_area_min = int(data['ls_area_min'])
    name = data['name']

    str = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %(is_circle, index, area, ls_circle, ls_convex, ls_ineria, ls_kernel, ls_kernel_cross, ls_area_max, ls_area_min, name)
    return str

    # 调用 camera_calibration 函数的示例参数
    #is_circle = True                             #检测十字架或圆   
    #index = 7                                    #标定板和打印点的规格  3, 5, 7, 9, 11, 27, 33, 37, 63
    #area = 5                                     #标定板尺寸
    #ls_circle = 0.1                              #圆度
    #ls_convex = 0.1                              #凸性
    #ls_ineria = 0.1                              #惯性
    #ls_kernel = 3                                #卷子核
    #ls_kernel_cross = 3                          #十子核
    #ls_area_max = 500000                         #最大面积
    #ls_area_min = 1                              #最小面积

    # 图像路径
    image_path = './1.jpg'
    rect_instance = (0, 0, 1080, 985)  # 你需要根据你的需求修改矩形区域

    try:
        success = lib.camera_calibration(
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
            ctypes.c_int(ls_area_min)
        )

        if success:
            return 'Camera calibration successful'
        else:
            return 'Camera calibration failed'
    except OSError as e:
      return f'Failed to call camera_calibration: {e}'
    except AttributeError as e:
      return f'Failed to find camera_calibration function: {e}'
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
