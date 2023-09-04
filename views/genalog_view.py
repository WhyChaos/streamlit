import sys
sys.path.append('../')

import streamlit as st
from PIL import Image, ImageEnhance
from effects.scan_effect import ScanEffect
from main2 import Opera
import os

from utils.convert_gray import convert_gray
from utils.download_image import download_image
from utils.download_json import download_json
    
from genalog.degradation.degrader import Degrader, ImageState
from utils.pillow_convert_opencv import pillow_to_opencv, opencv_to_pillow


def genalog_view(file):
    expander = st.sidebar.expander("效果选择")
    expander_col1, expander_col2 = expander.columns(2)
    select_blur = expander_col1.checkbox('blur', help='当扫描仪无法正确聚焦于文档时出现的效果，导致文档看起来有雾/模糊。')
    # select_bleed_through = expander_col2.checkbox('bleed_through', help='此效果试图模仿墨水从打印页面的一侧渗透到另一侧的情况。')
    select_morphology = expander_col2.checkbox('morphology', help='Dynamic 使用给定的参数调用不同的形态操作（“open”、“close”、“dilate”和“erode”）')
    select_pepper = expander_col1.checkbox('pepper', help='在 src 图像上随机散布暗像素。')
    select_salt = expander_col2.checkbox('salt', help='在 src 图像上随机散布白色像素')
    
    degradations = [
    ]
    
    if select_blur:
        blur_params = st.sidebar.expander('blur参数')
        blur_radius = blur_params.number_input(label='radius', min_value=0, max_value=50, value=5, help='方核的大小，必须是奇数。默认为 5', step=2)
        degradations.append(("blur", {"radius": blur_radius}))
    # if select_bleed_through:
    #     bleed_through_params = st.sidebar.expander('bleed_through参数')
    #     bleed_through_alpha = bleed_through_params.number_input(label='alpha', min_value=0.0, max_value=1.0, value=0.8, step=0.1, help='前景的透明因素。默认为0.8')
    #     bleed_through_gamma = bleed_through_params.number_input(label='gamma', min_value=0.0, max_value=1.0, value=0.0, step=0.1, help='亮度常数。默认为0。')
    #     bleed_through_offset_x = bleed_through_params.number_input(label='offset_x', min_value=-100, max_value=100, value=0, help='背景翻译偏移。 默认为 0。正值右移，负值右移。')
    #     bleed_through_offset_y = bleed_through_params.number_input(label='offset_y', min_value=-100, max_value=100, value=5, help='背景翻译偏移。 默认为 5。正值向下移动，负值向上移动。')
    #     degradations.append(("bleed_through", {
    #         "src": ImageState.CURRENT_STATE,
    #         "background": ImageState.ORIGINAL_STATE,
    #         "alpha": bleed_through_alpha,
    #         "gamma": bleed_through_gamma,
    #         "offset_x": bleed_through_offset_x,
    #         "offset_y": bleed_through_offset_y,
    #     }))
    if select_morphology:
        morphology_params = st.sidebar.expander('morphology参数')
        morphology_operation = morphology_params.selectbox(
            "operation ",
            ("open", "close", "dilate", "erode"),
            help='形态学操作的名称：（“open”、“close”、“dilate”、“erode”）默认为“open”。',
        )
        contmorphology_kernel_shape  = morphology_params.container()
        contmorphology_kernel_shape.write('kernel_shape')
        contmorphology_kernel_shape_columns = contmorphology_kernel_shape.columns(2)
        contmorphology_rows = contmorphology_kernel_shape_columns[0].number_input(label='rows', min_value=1, max_value=50, value=3)
        contmorphology_cols = contmorphology_kernel_shape_columns[1].number_input(label='cols', min_value=1, max_value=50, value=3)
        morphology_kernel_type = morphology_params.selectbox(
            "kernel_type",
            ("ones", "upper_triangle", "lower_triangle", "x", "plus", "ellipse") ,
            help='内核类型。 （“ones”、“upper_triangle”、“lower_triangle”、“x”、“plus”、“ellipse”）默认为“ones”。'
        )
        degradations.append(("morphology", {"operation": morphology_operation, "kernel_shape":(contmorphology_rows,contmorphology_cols), "kernel_type":morphology_kernel_type}),)
    if select_pepper:
        pepper_params = st.sidebar.expander('pepper参数')
        pepper_amount  = pepper_params.number_input(label='pepper_amount', min_value=0.0, max_value=1.0, value=0.05, help='应用效果的范围 [0, 1] 中的像素比例。 默认为 0.05。')
        degradations.append(("pepper", {"amount": pepper_amount}))
    if select_salt:
        salt_params = st.sidebar.expander('salt参数')
        salt_amount  = salt_params.number_input(label='salt_amount', min_value=0.0, max_value=1.0, value=0.05, help='应用效果的范围 [0, 1] 中的像素比例。 默认为 0.05。')
        degradations.append(("salt", {"amount": salt_amount}))
    
    
        
    keyword = st.sidebar.text_input('关键字(空格隔开)', '')
    keyword_type = st.sidebar.selectbox('打码效果', ('马赛克', '黑'))
    keyword_state = st.sidebar.checkbox("抹除一行")
    
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
    col2.subheader("扫描效果")
    
    if file is not None:
        # file = os.path.abspath(file)
        image = Image.open(file)
        
        # 处理图片=
        opera = Opera(keyword, keyword_state)
        image = opera.main(image, keyword_type)
        
        if len(degradations) > 0:
            degrader = Degrader(degradations)
            image = pillow_to_opencv(image)
            image = degrader.apply_effects(image)
            image = opencv_to_pillow(image)
            
        
        col2.image(image, caption="扫描效果", use_column_width=True)
        download_image(col2, image, "image")
        # json_data = {
        #     "option": "扫描",
        #     "is_gray": is_gray,
        #     "contrast_factor": contrast_factor,
        #     "brightness_factor": brightness_factor,
        #     "scan_line_probability": scan_line_probability,
        #     "black_scan_line_probability": black_scan_line_probability,
        #     "noise_probability": noise_probability,
        #     "black_noise_probability": black_noise_probability,
        #     "curve_effect": curve_effect,
        #     "keyword": keyword,
        #     "keyword_type": keyword_type,
        #     "keyword_state": keyword_state,
        # }
        # download_json(col2, json_data, 'data.json')
    else:
        col2.info("请上传一张图片")