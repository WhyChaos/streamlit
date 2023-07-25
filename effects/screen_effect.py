
import cv2
import numpy as np
from PIL import Image
import random


class ScreenEffect:
    def __init__(self):
        # 背景图，四个坐标：左上，右上，右下，左下
        self.screen = [
            'moier1.jpg', 'moier2.jpg', 'moier3.jpg'
        ]
        self.background_path = 'effects/screen/'

    def main(self, image, moier_weight, moier_type, light_weight):
        # 将Pillow的Image对象转换为NumPy数组
        image_array = np.array(image)
        # # 将NumPy数组从RGB模式转换为BGR模式
        # bgr_image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        # 将NumPy数组转换为OpenCV的图像对象
        image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

        height, width, _ = image.shape

        # screen_index = random.randint(0, len(self.screen)-1)
        screen_index = int(moier_type[-1])-1

        # 加载屏幕
        moier = cv2.imread(self.background_path + self.screen[screen_index])
        moier = cv2.resize(moier, (width, height))

        # 将背景图像与透视变换后的图像相结合
        result = cv2.bitwise_and(moier, image)
        result = cv2.addWeighted(image, 1-moier_weight, moier, moier_weight, light_weight)

        # 将OpenCV图像对象转换为RGB模式
        rgb_image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        # 创建Pillow的Image对象
        result = Image.fromarray(rgb_image)

        return result
