import sys
sys.path.append('../')

import streamlit as st
from PIL import Image, ImageEnhance
from effects.scan_effect import ScanEffect
from main2 import Opera
from utils.edit_image import Mark, Rotate
import os

from utils.convert_gray import convert_gray
    
    


def edit_view(file):
    is_gray = st.sidebar.checkbox("转为灰度(黑白)")
    # 对比度和亮度
    expander1 = st.sidebar.expander("图像增强(参数10为原图像)")
    contrast_factor = expander1.slider('对比度', 0, 100, 10)
    brightness_factor = expander1.slider('亮度', 0, 100, 10)
    color_factor = expander1.slider('色彩平衡', 0, 100, 10)
    sharpness_factor = expander1.slider('清晰度', 0, 100, 10)
    # 遮挡效果
    expander2 = st.sidebar.expander("遮挡")
    keyword = expander2.text_input('关键字(空格隔开)', '')
    keyword_type = expander2.selectbox('遮挡效果', ('马赛克', '黑'))
    keyword_state = expander2.checkbox("作用关键词的一行")
    # 标注效果
    expander3 = st.sidebar.expander("标注")
    mark_keyword = expander3.text_input('关键字(空格隔开)', '', key='mark_keyword')
    mark_type = expander3.selectbox('标注效果', ('框', '下划线', '斜线', '椭圆'), key='mark_type')
    mark_width = expander3.slider('标注线宽度', 1, 10, 2)
    mark_color = expander3.color_picker('标注', '#F90000')
    mark_keyword_state = expander3.checkbox("作用关键词的一行", key='mark_keyword_state')
    # 旋转
    expander4 = st.sidebar.expander("旋转")
    rotate_angle = expander4.slider('角度', 0, 359, 0)
    rotate_expand = expander4.checkbox("保持原比例")
    rotate_fillcolor = expander4.color_picker('填充颜色', '#000000')

    
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
    col2.subheader("效果")
    
    if file is not None:
        # file = os.path.abspath(file)
        image = Image.open(file)
        #灰度
        if is_gray:
            image = convert_gray(image)
        # 亮度和对比度
        effect = ScanEffect()
        image = effect.apply_scan_brightness_effect(image=image, factor=brightness_factor/10.0)
        image = effect.apply_scan_contrast_effect(image=image, factor=contrast_factor/10.0)
        image = effect.apply_color_enhance(image=image, factor=color_factor/10.0)
        image = effect.apply_sharpness_enhance(image=image, factor=sharpness_factor/10.0)
        # 遮挡
        opera = Opera(keyword, keyword_state)
        image = opera.main(image, keyword_type)
        # 标注
        mark = Mark(mark_keyword, mark_keyword_state)
        image = mark.apply_mark(image=image, mark_type=mark_type, mark_color=mark_color, mark_width=mark_width)
        # 旋转
        rotate = Rotate()
        image = rotate.apply(image, rotate_angle, rotate_expand, rotate_fillcolor)
        
        col2.image(image, caption="效果", use_column_width=True)
    else:
        col2.info("请上传一张图片")