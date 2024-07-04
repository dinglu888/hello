import ctypes
import cv2
import numpy as np

# 加载共享库
try:
    lib = ctypes.CDLL('./libgalvanometer_correction.so')
    print("Library loaded successfully")
except OSError as e:
    print(f"Failed to load library: {e}")

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

lib.galvanometer_correction.argtypes = [
    ctypes.c_char_p,  # const char* (as img_path)
    ctypes.POINTER(ctypes.c_int),  # int* (as rect array)
    ctypes.c_int,  # int (index)
    ctypes.c_bool,  # bool (is_circle)
    ctypes.c_double,  # double (ls_circle)
    ctypes.c_double,  # double (ls_convex)
    ctypes.c_double,  # double (ls_ineria)
    ctypes.c_double,  # double (ls_kernel)
    ctypes.c_int,  # int (ls_kernel_cross)
    ctypes.c_int,  # int (ls_area_max)
    ctypes.c_int   # int (ls_area_min)
]
lib.galvanometer_correction.restype = ctypes.POINTER(ctypes.c_float)

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

# 调用 camera_calibration 函数的示例参数
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

# 图像路径
image_path = '1.jpg'

print("# Call camera_calibration function")
try:
    rect_instance = (0, 0, 1280, 1280)  # 你需要根据你的需求修改矩形区域
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
        print("Camera calibration successful")
    else:
        print("Camera calibration failed")
except OSError as e:
    print(f"Failed to call camera_calibration: {e}")
except AttributeError as e:
    print(f"Failed to find camera_calibration function: {e}")

# 调用 galvanometer_correction 函数的示例参数
is_circle2 = True
index2 = 0
area2 = 5
ls_circle2 = 0.2
ls_convex2 = 0.2
ls_ineria2 = 0.2
ls_kernel2 = 3
ls_kernel_cross2 = 3
ls_area_max2 = 5000
ls_area_min2 = 1

# 图像路径
image_path2 = 'h.jpg'

print("# Call galvanometer_correction function")
try:
    rect_instance2 = (0, 0, 1200, 1200)  # 你需要根据你的需求修改矩形区域
    result_ptr = lib.galvanometer_correction(
        image_path2.encode('utf-8'),
        cv_rect_to_c_int_ptr(rect_instance2),
        ctypes.c_int(index2),
        ctypes.c_bool(is_circle2),
        ctypes.c_double(ls_circle2),
        ctypes.c_double(ls_convex2),
        ctypes.c_double(ls_ineria2),
        ctypes.c_double(ls_kernel2),
        ctypes.c_int(ls_kernel_cross2),
        ctypes.c_int(ls_area_max2),
        ctypes.c_int(ls_area_min2)
    )
    if result_ptr:
        # 将结果解析为 NumPy 数组
        result_size = loc_get_size(index2) * 2  # 根据你的需求设置数组大小
        result_array = ctypes.cast(result_ptr, ctypes.POINTER(ctypes.c_float * result_size)).contents
        m_result = np.ctypeslib.as_array(result_array)
        m_result = m_result.astype(np.float32)
        output_txt('output.txt', m_result)
        # 直接打印数组
        print("Result array:", m_result)
        print("Galvanometer correction successful")
    else:
        print("Galvanometer correction failed")
except OSError as e:
    print(f"Failed to call galvanometer_correction: {e}")
except AttributeError as e:
    print(f"Failed to find galvanometer_correction function: {e}")

