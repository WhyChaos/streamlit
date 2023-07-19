import streamlit as st
from PIL import Image, ImageEnhance
from effects.scan_effect import ScanEffect
from main2 import Opera
import os


def convert_gray(image):
     # 获取图像的宽度和高度
    width, height = image.size

    # 创建一个新的空白图像，模式为RGB
    black_and_white_image = Image.new("RGB", (width, height))

    # 遍历图像的每个像素，并将其设置为黑白颜色
    for x in range(width):
        for y in range(height):
            # 获取原图像像素的颜色
            r, g, b = image.getpixel((x, y))
            # 计算灰度值
            gray = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
            # 将新图像的像素设置为灰度值
            black_and_white_image.putpixel((x, y), (gray, gray, gray))

    return black_and_white_image
    
    


def scan_view(file):
    is_gray = st.sidebar.checkbox("转为灰度(黑白)")
    scan_line_probability = st.sidebar.number_input(label='扫描线概率(%)', min_value=0, max_value=100, value=1)
    if scan_line_probability > 0:
        black_scan_line_probability = st.sidebar.slider("黑扫描线概率(%)", 0, 100, 50)
    noise_line_probability = st.sidebar.number_input(label='噪点概率(‰)', min_value=0, max_value=1000, value=1)
    if noise_line_probability > 0:
        black_noise_line_probability = st.sidebar.slider("黑噪点概率(%)", 0, 100, 50)
    curve_effect = st.sidebar.selectbox('蜷曲效果', ('纸张弯曲1', '纸张弯曲2', '纸张平整'))
    contrast_factor = st.sidebar.slider('对比度(*10)', 1, 100, 10)
    brightness_factor = st.sidebar.slider('亮度(*10)', 1, 100, 10)
    keyword = st.sidebar.text_input('关键字(空格隔开)', '先秦 中国')
    keyword_type = st.sidebar.selectbox('打码效果', ('马赛克', '黑'))
    keyword_state = st.sidebar.checkbox("抹除一行")
    
    # 在右侧展示原始图片和处理后的图片
    col1, col2 = st.columns(2)
    # 展示原始图片
    col1.subheader("原始图片")
    if file is not None:
        image = Image.open(file)
        col1.image(image, caption="原始图片", use_column_width=True)
    else:
        col1.info("请上传一张图片")
    # 处理图片并展示处理后的图片
    col2.subheader("扫描效果")
    
    if file is not None:
        # file = os.path.abspath(file)
        image = Image.open(file)
        #灰度
        if is_gray:
            image = convert_gray(image)
        
        # 处理图片=
        opera = Opera(keyword, keyword_state)
        image = opera.main(image, keyword_type)
        effect = ScanEffect()
        if scan_line_probability > 0:
            image = effect.apply_scan_line_effect(image=image, probability=scan_line_probability/100.0, black_probability=black_scan_line_probability/100.0)
        if noise_line_probability > 0:
            image = effect.apply_scan_noise_effect(image=image, probability=noise_line_probability/1000.0, black_probability=black_noise_line_probability/100.0)
        image = effect.apply_scan_brightness_effect(image=image, factor=brightness_factor/10.0)
        image = effect.apply_scan_contrast_effect(image=image, factor=contrast_factor/10.0)
        if curve_effect != '纸张平整':
            image = effect.apply_scan_curve_effect(image=image, type=int(curve_effect[-1]))
        col2.image(image, caption="扫描效果", use_column_width=True)
    else:
        col2.info("请上传一张图片")