import cv2
import numpy as np
from PIL import Image

def pillow_to_opencv(image):
    image_array = np.array(image)
    # # 将NumPy数组从RGB模式转换为BGR模式
    # bgr_image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    # 将NumPy数组转换为OpenCV的图像对象
    image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

    return image
    
def opencv_to_pillow(image):
    # 将OpenCV图像对象转换为RGB模式
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 创建Pillow的Image对象
    image = Image.fromarray(rgb_image)
    
    return image