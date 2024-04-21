import sys
sys.path.append('../')

import streamlit as st
from PIL import Image, ImageEnhance
from effects.photo_effect import PhotoEffect
from main2 import Opera
import os

from utils.convert_gray import convert_gray
from utils.download_image import download_image
from utils.download_json import download_json

from utils.detect_a4_corners import detect_a4_corners
 
def photo_view(file):
    background_type = st.sidebar.selectbox('背景图', ('随机', '自定义'))
    if background_type == '自定义':
        # is_detect_a4_corners = st.sidebar.checkbox("检测A4角")
        background_file = st.sidebar.file_uploader("上传背景图", type=["jpg", "jpeg", "png"])
        syncopated_projection_params = st.sidebar.expander('切分投影参数')
        syncopated_projection_columns = syncopated_projection_params.columns(2)
        syncopated_projection_x = syncopated_projection_columns[0].number_input(label='水平切分数', min_value=1, max_value=10, value=1, step=1, help='水平方向切分为几块')
        syncopated_projection_y = syncopated_projection_columns[1].number_input(label='垂直切分数', min_value=1, max_value=10, value=1, step=1, help='垂直方向切分为几块')
        if background_file is not None:
            background_image = Image.open(background_file)
            
        

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
    if file!=None and (background_type=='随机' or background_file!=None):
        image = Image.open(file)
        # 处理图片=
        if background_type == '随机':
            image = effect.main(image=image)
        elif background_type == '自定义':
            image = effect.main2(int(syncopated_projection_x), int(syncopated_projection_y), image=image, background_file=background_file, background_image=background_image)
        
        col2.image(image, caption="拍照效果", use_column_width=True)
        download_image(col2, image, "image")
    else:
        col2.info("请上传一张图片") 