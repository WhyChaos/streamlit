import streamlit as st
from PIL import Image, ImageEnhance
from effects.photo_effect import PhotoEffect
from main2 import Opera
import os

 
def photo_view(file):
    background_type = st.sidebar.selectbox('背景图', ('随机', '自定义'))
    if background_type == '自定义':
        pass
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
    col2.subheader("拍照效果")
    
    effect = PhotoEffect()
    if file is not None:
        image = Image.open(file)
        # 处理图片=
        opera = Opera(keyword)
        image = opera.main(image, keyword_type)
        if background_type == '随机':
            image = effect.main(image=image)
        col2.image(image, caption="拍照效果", use_column_width=True)
    else:
        col2.info("请上传一张图片")