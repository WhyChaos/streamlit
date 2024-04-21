import streamlit as st
from PIL import Image, ImageEnhance
from main2 import Opera
import os
from views.scan_view import scan_view
from views.photo_view import photo_view
from views.photo_screen_view import photo_screen_view
from views.screen_view import screen_view
from views.json_view import json_view
from views.genalog_view import genalog_view
from views.test_view import test_view
from views.background_view import background_view
from views.augraphy_view import augraphy_view
from views.edit_view import edit_view

def main():
    # 设置页面标题
    # st.title("图片处理应用")
    st.sidebar.title('图像场景仿真')
    # 在左侧栏添加输入参数
    st.sidebar.header("输入参数")
    file = st.sidebar.file_uploader("上传图片", type=["jpg", "jpeg", "png"])
    option = st.sidebar.selectbox(
        '效果选择',
        # ('图片编辑', '效果模拟', '模拟拍照', '扫描1', '扫描2', '拍照（屏幕)', '屏幕', '添加背景', '上传json', 'test'))
        ('图片编辑', '效果模拟', '模拟拍照'))

    if option == '图片编辑':
        edit_view(file)
    if option == '扫描1':
        scan_view(file)
    elif option == '模拟拍照':
        photo_view(file)
    elif option == '拍照（屏幕)':
        photo_screen_view(file)
    elif option == '屏幕':
        screen_view(file)
    elif option == '上传json':
        json_view(file)
    elif option == '扫描2':
        genalog_view(file)
    elif option == 'test':
        test_view(file)
    elif option == '添加背景':
        background_view(file)
    elif option == '效果模拟':
        augraphy_view(file)



if __name__ == '__main__':
    # st.set_option("server.port", 8000)
    # st.set_option("server.baseUrl", "/pic")
    main()