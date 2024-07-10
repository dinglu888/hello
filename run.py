import os
import ctypes
import numpy as np
import requests

from flask import Flask, request, jsonify, json
from ctypes import *
from PIL import Image

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
    #data = {"name":"xiaoming", "age":"18"}
    #return data;
    url = 'https://7072-prod-0gwkiow3d05ece9c-1327429310.tcb.qcloud.la/img/1720487782502.jpg'
    response = requests.get(url)
    if response.status_code == 200:
        with open('./abc.jpg', 'wb') as f:
            f.write(response.content)
        return 'download success'
    else:
        return 'request fail'

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
        ctypes.c_double,  # double (ls_circle)
        ctypes.c_double,  # double (ls_convex)
        ctypes.c_double,  # double (ls_ineria)
        ctypes.c_int,  # int (ls_kernel)
        ctypes.c_int,  # int (ls_kernel_cross)
        ctypes.c_int,  # int (ls_area_max)
        ctypes.c_int,   # int (ls_area_min)
        ctypes.c_double  # double (area)
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
    name = str(data['img_name'])
    width = int(data['img_width'])
    height = int(data['img_height'])

    #str = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %(is_circle, index, area, ls_circle, ls_convex, ls_ineria, ls_kernel, ls_kernel_cross, ls_area_max, ls_area_min, name,width,height)
    #return str

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

    url = 'https://7072-prod-0gwkiow3d05ece9c-1327429310.tcb.qcloud.la/img/' + name + '.jpg'
    image_path = f'./1_{name}.jpg'
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
    else:
        return 'download fail'
    
    image = Image.open(image_path)
    width1, height1 = image.size
    rect_instance = (0, 0, width1, height1)  # 你需要根据你的需求修改矩形区域
    return f'image size is {width1},{height1}'

    try:
        success = lib.camera_calibration(
            image_path.encode('utf-8'),
            cv_rect_to_c_int_ptr(rect_instance),
            ctypes.c_bool(is_circle),
            ctypes.c_int(index),
            ctypes.c_double(ls_circle),
            ctypes.c_double(ls_convex),
            ctypes.c_double(ls_ineria),
            ctypes.c_int(ls_kernel),
            ctypes.c_int(ls_kernel_cross),
            ctypes.c_int(ls_area_max),
            ctypes.c_int(ls_area_min),
            ctypes.c_double(area)
        )

        if success:
            return 'Camera calibration successful'
        else:
            return 'Camera calibration failed'
    except OSError as e:
      return f'Failed to call camera_calibration: {e}'
    except AttributeError as e:
      return f'Failed to find camera_calibration function: {e}'

##########################################################
   
@app.route('/galvanometer_correction', methods=['POST'])
def galvanometer_correction():
    try:
        lib = ctypes.CDLL('./libgalvanometer_correction.so')
        #return 'Library loaded successfully'
    except OSError as e:
        return f'Failed to load library:{e}'
        
        
    lib.galvanometer_correction.argtypes = [
        ctypes.c_char_p,  # const char* (as img_path)
        ctypes.POINTER(ctypes.c_int),  # int* (as rect array)
        ctypes.c_bool,  # bool (is_circle)
        ctypes.c_int,  # int (index)     
        ctypes.c_double,  # double (ls_circle)
        ctypes.c_double,  # double (ls_convex)
        ctypes.c_double,  # double (ls_ineria)
        ctypes.c_int,  # int (ls_kernel)
        ctypes.c_int,  # int (ls_kernel_cross)
        ctypes.c_int,  # int (ls_area_max)
        ctypes.c_int   # int (ls_area_min)
    ]
    lib.galvanometer_correction.restype = ctypes.POINTER(ctypes.c_float)

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
    name = str(data['img_name'])
    width = int(data['img_width'])
    height = int(data['img_height'])

    #str = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %(is_circle, index, area, ls_circle, ls_convex, ls_ineria, ls_kernel, ls_kernel_cross, ls_area_max, ls_area_min, name,width,height)
    #return str

    #调用 camera_calibration 函数的示例参数
    #is_circle = True                             #检测十字架或圆   
    #index = 0                                    #标定板和打印点的规格  3, 5, 7, 9, 11, 27, 33, 37, 63
    #area = 5                                     #标定板尺寸
    #ls_circle = 0.2                              #圆度
    #ls_convex = 0.2                              #凸性
    #ls_ineria = 0.2                              #惯性
    #ls_kernel = 3                                #卷子核
    #ls_kernel_cross = 3                          #十子核
    #ls_area_max = 50000                         #最大面积
    #ls_area_min = 1                              #最小面积

    url = 'https://7072-prod-0gwkiow3d05ece9c-1327429310.tcb.qcloud.la/img/' + name + '.jpg'
    image_path = f'./2_{name}.jpg'
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
    else:
        return 'download fail'

    rect_instance = (0, 0, width, height)  # 你需要根据你的需求修改矩形区域

    try:
        result_ptr = lib.galvanometer_correction(
            image_path.encode('utf-8'),
            cv_rect_to_c_int_ptr(rect_instance),
            ctypes.c_bool(is_circle),
            ctypes.c_int(index),
            ctypes.c_double(ls_circle),
            ctypes.c_double(ls_convex),
            ctypes.c_double(ls_ineria),
            ctypes.c_int(ls_kernel),
            ctypes.c_int(ls_kernel_cross),
            ctypes.c_int(ls_area_max),
            ctypes.c_int(ls_area_min)
        )

        if result_ptr is None:
            return 'Galvanometer correction failed'
        else:      
            # 将结果解析为 NumPy 数组
            result_size = loc_get_size(index) * 2  # 根据你的需求设置数组大小
            result_array = ctypes.cast(result_ptr, ctypes.POINTER(ctypes.c_float * result_size)).contents
            m_result = np.ctypeslib.as_array(result_array)
            m_result = m_result.astype(np.float32)
            output_txt('output.txt', m_result)
            #return 'Galvanometer correction successful'

            with open('output.txt', 'r') as file:
                content = file.read()

            return jsonify(content)
            
    except OSError as e:
      return f'Failed to call galvanometer_correction: {e}'
    except AttributeError as e:
      return f'Failed to find galvanometer_correction function: {e}'
    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
