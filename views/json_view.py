import sys
sys.path.append('../')

import streamlit as st
from PIL import Image, ImageEnhance
from effects.screen_effect import ScreenEffect
from main2 import Opera
import os
from utils.convert_gray import convert_gray
from utils.download_image import download_image
from utils.download_json import download_json

import json

from utils.effect_operate import main as effect_operate
 
def json_view(file):
    json_file = st.sidebar.file_uploader("上传效果json", type=["json"])
    
    # 在右侧展示原始图片和处理后的图片
    col1, col2 = st.columns(2)
    # 展示原始图片
    col1.subheader("原始图片")
    if file is not None:
        origin_image = Image.open(file)
        col1.image(origin_image, caption="原始图片", use_column_width=True)
    else:
        col1.info("请上传一张图片")
    # 处理图片并展示处理后的图片
    col2.subheader("拍照效果")
    
    if json_file is not None and file is not None:
        
        # 读取上传的JSON文件内容
        content = json_file.read()
        try:
            # 解析JSON数据
            data_json = json.loads(content)
            # st.sidebar.success("JSON file successfully parsed!")

            image = Image.open(file)
            
            image = effect_operate(data_json, image = image)
            
            col2.image(image, caption="扫描效果", use_column_width=True)
            
            # # 显示解析后的数据
            st.sidebar.write("Parsed JSON data:")
            st.sidebar.write(data_json)

        except json.JSONDecodeError:
            st.sidebar.error("Error parsing JSON file. Please make sure it's a valid JSON file.")
        except Exception as e:
            st.sidebar.error(f"An error occurred: {e}")
            # st.sidebar.error("json格式有误！")
        
        # image = Image.open(file)s
        
        # download_image(col2, image, "image")
    else:
        col2.info("请上传一张图片")