import streamlit as st
from PIL import Image, ImageEnhance
from effects.scan_effect import ScanEffect
from main2 import Opera
import os


def scan_view(file):
    scan_line_probability = st.sidebar.number_input(label='扫描线概率(%)', min_value=0, max_value=100, value=1)
    if scan_line_probability > 0:
        black_scan_line_probability = st.sidebar.slider("黑扫描线概率(%)", 0, 100, 50)
    noise_line_probability = st.sidebar.number_input(label='噪点概率(‰)', min_value=0, max_value=1000, value=1)
    if noise_line_probability > 0:
        black_noise_line_probability = st.sidebar.slider("黑噪点概率(%)", 0, 100, 50)
    curve_effect = st.sidebar.selectbox('蜷曲效果', ('效果1', '效果2', '无'))
    keyword = st.sidebar.text_input('关键字(空格隔开)', '先秦 中国')
    keyword_type = st.sidebar.selectbox('打码效果', ('马赛克', '黑'))
    
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
        
        # 处理图片=
        opera = Opera(keyword)
        image = opera.main(image, keyword_type)
        effect = ScanEffect()
        if scan_line_probability > 0:
            image = effect.apply_scan_line_effect(image=image, probability=scan_line_probability/100.0, black_probability=black_scan_line_probability/100.0)
        if noise_line_probability > 0:
            image = effect.apply_scan_noise_effect(image=image, probability=noise_line_probability/1000.0, black_probability=black_noise_line_probability/100.0)
        if curve_effect != '无':
            image = effect.apply_scan_curve_effect(image=image, type=int(curve_effect[-1]))
        col2.image(image, caption="扫描效果", use_column_width=True)
    else:
        col2.info("请上传一张图片")