import cv2
import numpy as np
import sys
sys.path.append('../')

from utils.pillow_convert_opencv import pillow_to_opencv

def detect_a4_corners(image):
    if image is None:
        raise ValueError("无法读取图像，请检查图像路径是否正确。")
    
    image = pillow_to_opencv(image)
    

    # 将图像转换为灰度图
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 对灰度图进行高斯模糊，以减少噪声
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # 使用Canny边缘检测算法
    edges = cv2.Canny(blurred_image, 50, 150)

    # 在边缘图上寻找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到面积最大的轮廓（假设这是A4纸的轮廓）
    max_contour = max(contours, key=cv2.contourArea)

    # 对轮廓进行逼近，以减少顶点数量
    epsilon = 0.02 * cv2.arcLength(max_contour, True)
    approx_corners = cv2.approxPolyDP(max_contour, epsilon, True)

    # 返回A4纸的四个角的坐标
    
    if len(approx_corners) < 4:
        return None
    
    # 假设坐标存储在一个列表coords中，每个坐标都是一个元组 (x, y)

    # 初始化左上、右上、右下和左下的坐标
    left_top = (approx_corners[0][0][0], approx_corners[0][0][1])
    right_top = (approx_corners[0][0][0], approx_corners[0][0][1])
    right_bottom = (approx_corners[0][0][0], approx_corners[0][0][1])
    left_bottom = (approx_corners[0][0][0], approx_corners[0][0][1])

    # 遍历坐标列表，找到相应的坐标
    for tmp in approx_corners:
        x, y = tmp[0]
        if x + y < left_top[0] + left_top[1]:
            left_top = (x, y)
        if x - y > right_top[0] - right_top[1]:
            right_top = (x, y)
        if x + y > right_bottom[0] + right_bottom[1]:
            right_bottom = (x, y)
        if x - y < left_bottom[0] - left_bottom[1]:
            left_bottom = (x, y)

    corners = []
    corners.append(left_top)
    corners.append(right_top)
    corners.append(right_bottom)
    corners.append(left_bottom)
    
    return corners

