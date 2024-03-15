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
    is_gray = st.sidebar.checkbox("转为灰度(黑白)")
    background_type = st.sidebar.selectbox('背景图', ('随机', '自定义'))
    if background_type == '自定义':
        # is_detect_a4_corners = st.sidebar.checkbox("检测A4角")
        background_file = st.sidebar.file_uploader("上传背景图", type=["jpg", "jpeg", "png"])
        if background_file is not None:
            background_image = Image.open(background_file)
        
        
    keyword = st.sidebar.text_input('关键字(空格隔开)', '')
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
    col2.subheader("拍照效果")
    
    effect = PhotoEffect()
    if file!=None and (background_type=='随机' or background_file!=None):
        image = Image.open(file)
        # 处理图片=
        #灰度
        if is_gray:
            image = convert_gray(image)
            
        opera = Opera(keyword, keyword_state)
        image = opera.main(image, keyword_type)
        if background_type == '随机':
            image = effect.main(image=image)
        elif background_type == '自定义':
            cut_columns = st.sidebar.columns(2)
            cut_x = cut_columns[0].number_input(label='x', min_value=1, max_value=10, value=1, step=1, help='横轴方向切分为几块')
            cut_y = cut_columns[1].number_input(label='y', min_value=1, max_value=10, value=1, step=1, help='横轴方向切分为几块')
            image = effect.main2(int(cut_x), int(cut_y), image=image, background_file=background_file, background_image=background_image)
        
        col2.image(image, caption="拍照效果", use_column_width=True)
        download_image(col2, image, "image")
        if background_type!='自定义':
            json_data = {
                "option": "拍照",
                "is_gray": is_gray,
                "keyword": keyword,
                "keyword_type": keyword_type,
                "keyword_state": keyword_state,
            }
            download_json(col2, json_data, 'data.json')
    else:
        col2.info("请上传一张图片") 