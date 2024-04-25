import sys
sys.path.append('../')

import streamlit as st
from PIL import Image, ImageEnhance
from effects.background_effect import BackgroundEffect
from main2 import Opera
import os
import random

from utils.convert_gray import convert_gray
from utils.download_image import download_image
from utils.download_json import download_json

from utils.detect_a4_corners import detect_a4_corners

from utils.pillow_convert_opencv import pillow_to_opencv, opencv_to_pillow
 
def background_view(file):
    is_gray = st.sidebar.checkbox("转为灰度(黑白)")
    background_file = st.sidebar.file_uploader("上传背景图", type=["jpg", "jpeg", "png"])
    
    if background_file is not None:
        background_image = Image.open(background_file)
        sidebar_col1, sidebar_col2 = st.sidebar.columns(2)
        width, height = background_image.size
        coordinate = {}
        
        # coordinate['x1'] = sidebar_col1.slider("左上(x坐标)", 0, width, random.randint(0, int(width/4)))
        # coordinate['y1'] = sidebar_col2.slider("左上(y坐标)", 0, height, random.randint(0, int(height/4)))
        # coordinate['x2'] = sidebar_col1.slider("右上(x坐标)", 0, width*2, random.randint(int(width/4)*3, width))
        # coordinate['y2'] = sidebar_col2.slider("右上(y坐标)", 0, height, random.randint(0, int(height/4)))
        # coordinate['x3'] = sidebar_col1.slider("右下(x坐标)", 0, width*2, random.randint(int(width/4)*3, width))
        # coordinate['y3'] = sidebar_col2.slider("右下(y坐标)", 0, height*2, random.randint(int(height/4)*3, height))
        # coordinate['x4'] = sidebar_col1.slider("左下(x坐标)", 0, width, random.randint(0, int(width/4)))
        # coordinate['y4'] = sidebar_col2.slider("左下(y坐标)", 0, height*2, random.randint(int(height/4)*3, height))
        coordinate['x1'] = random.randint(0, int(width/4))
        coordinate['y1'] = random.randint(0, int(height/4))
        coordinate['x2'] = random.randint(int(width/4)*3, width)
        coordinate['y2'] = random.randint(0, int(height/4))
        coordinate['x3'] = random.randint(int(width/4)*3, width)
        coordinate['y3'] = random.randint(int(height/4)*3, height)
        coordinate['x4'] = random.randint(0, int(width/4))
        coordinate['y4'] = random.randint(int(height/4)*3, height)
        
        expander = st.sidebar.expander("背景操作")
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
        image = Image.open(file)
        col1.image(image, caption="原始图片", use_column_width=True)
    else:
        col1.info("请上传一张图片")
    # 处理图片并展示处理后的图片
    col2.subheader("拍照效果")
    
    effect = BackgroundEffect()
    if file!=None and background_file!=None:
        image = Image.open(file)
        # 处理图片=
        #灰度
        if is_gray:
            image = convert_gray(image)
            
        if len(degradations) > 0:
            degrader = Degrader(degradations)
            background_image = pillow_to_opencv(background_image)
            background_image = degrader.apply_effects(background_image)
            background_image = opencv_to_pillow(background_image)
            
        opera = Opera(keyword, keyword_state)
        image = opera.main(image, keyword_type)
        image = effect.main2(image=image, background_file=background_file, coordinate=coordinate, background_image=background_image)
        col2.image(image, caption="拍照效果", use_column_width=True)
        download_image(col2, image, "image")
        # if background_type!='自定义':
        #     json_data = {
        #         "option": "拍照",
        #         "is_gray": is_gray,
        #         "keyword": keyword,
        #         "keyword_type": keyword_type,
        #         "keyword_state": keyword_state,
        #     }
        #     download_json(col2, json_data, 'data.json')
    else:
        col2.info("请上传一张图片") 