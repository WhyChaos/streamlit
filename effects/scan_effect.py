
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import random
import numpy as np
import math


class ScanEffect:
    def apply_scan_line_effect(self, image, probability=0.01, black_probability=0.5):
        # 创建新的图像，与原图像大小相同
        new_image = Image.new("RGB", image.size)
        draw = ImageDraw.Draw(new_image)
        width, height = image.size
        # 遍历每个扫描线
        for y in range(0, height):
            # 是否为扫描线
            scan_line = random.random() < probability
            # 绘制偏斜后的扫描线
            for x in range(width):
                if scan_line:
                    # 白扫描线和黑扫描线概率各50%
                    if random.random() < black_probability:
                        pixel = (0, 0, 0)
                    else:
                        pixel = (255, 255, 255)
                else:
                    pixel = image.getpixel((x, y))

                # 在新图像上绘制像素
                draw.point((x, y), pixel)

        return new_image

    def apply_scan_noise_effect(self, image, probability=0.001, black_probability=0.5):
        # 创建新的图像，与原图像大小相同
        new_image = Image.new("RGB", image.size)
        draw = ImageDraw.Draw(new_image)
        width, height = image.size
        # 遍历
        for y in range(0, height):
            for x in range(width):
                scan_noise = random.random() < probability
                if scan_noise:
                    # 白和黑概率各50%
                    if random.random() < black_probability:
                        pixel = (0, 0, 0)
                    else:
                        pixel = (255, 255, 255)
                else:
                    pixel = image.getpixel((x, y))

                # 在新图像上绘制像素
                draw.point((x, y), pixel)

        return new_image

    def apply_scan_curve_effect(self, image, type=1):
        width = image.width
        height = image.height
        
        if type==1:
            curve_x = np.linspace(1, 5, width)
            curve_y = np.sin(curve_x) / curve_x * height / 50
        elif type==2:
            curve_x = np.linspace(1, 5, width)
            curve_y = np.cos(curve_x) / curve_x * height / 50
        
        
        new_image = Image.new("RGB", image.size)
        draw = ImageDraw.Draw(new_image)

        for i, x in enumerate(range(width)):
            for y in range(height):
                offset_y = math.ceil(curve_y[i]) + y
                if offset_y >= 0 and offset_y < height:
                    pixel = image.getpixel((x, offset_y))
                else:
                    pixel = (255, 255, 255)
                draw.point((x, y), pixel)

        return new_image
