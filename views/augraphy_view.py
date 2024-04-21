import sys
sys.path.append('../')

import cv2
import streamlit as st
from PIL import Image, ImageEnhance
from effects.scan_effect import ScanEffect
from main2 import Opera
import os
import numpy as np

from utils.convert_gray import convert_gray
from utils.download_image import download_image
from utils.download_json import download_json
    
# from augraphy import AugraphyPipeline, BadPhotoCopy, BindingsAndFasteners, BleedThrough, Brightness, BrightnessTexturize, ColorPaper, ColorShift, DirtyScreen
from augraphy import *
from utils.pillow_convert_opencv import pillow_to_opencv, opencv_to_pillow


def augraphy_view(file):
    expander = st.sidebar.expander("效果选择")
    expander_col1, expander_col2 = expander.columns(2)
    
    select_BleedThrough  = expander_col1.checkbox('墨水渗透', help='模拟墨水出血和高斯模糊操作组合的渗透效果。')
    select_BrightnessTexturize = expander_col2.checkbox('纸张纹理', help='在亮度通道中创建随机噪声以模拟纸张纹理。')
    select_ColorShift = expander_col1.checkbox('偏移', help='将每个 BGR 颜色通道移动一定的偏移量以创建移动的颜色效果。')
    select_DirtyDrum = expander_col2.checkbox('脏滚筒', help='模拟脏滚筒')
    select_DirtyRollers = expander_col2.checkbox('扫描阴影', help='模拟某些文档扫描仪创建的效果')
    
    select_DotMatrix = expander_col1.checkbox('点阵效果', help='通过在检测到的轮廓中绘制平均颜色的点来创建点阵效果。')
    # select_DoubleExposure = expander_col2.checkbox('双曝光', help='模拟手机摄像头拍照时的双重曝光效果。')
    
    
    select_Faxify = expander_col2.checkbox('传真效果', help='模拟图像中的传真效果。')
    select_InkColorSwap = expander_col1.checkbox('墨水颜色交换', help='根据检测到的墨水轮廓交换图像中墨水的颜色')
    select_Jpeg = expander_col2.checkbox('JPEG压缩', help='使用 JPEG 编码在图像中创建压缩伪影。')
    select_LightingGradient = expander_col1.checkbox('光照渐变', help='生成由给定位置和方向的光带生成的衰减光蒙版，并将其作为照明或亮度梯度应用于图像。')
    select_LowInkPeriodicLines = expander_col1.checkbox('扫描线', help='创建一组在整个图像中以周期性方式重复的线条。')
    select_Markup = expander_col2.checkbox('标注', help='使用轮廓检测​​来检测文本行并添加平滑的文本删除线、突出显示或下划线效果。')
    select_NoiseTexturize = expander_col1.checkbox('纸张纹理', help='创建随机噪声图案来模拟纸张纹理')
    select_NoisyLines = expander_col2.checkbox('线条噪声', help='通过以固定间隔绘制水平或垂直线来创建嘈杂的线条。')
    select_ReflectedLight = expander_col1.checkbox('反射光', help='通过绘制不同亮度的椭圆来创建反射光效果。')
    select_Scribbles = expander_col2.checkbox('涂鸦', help='将涂鸦应用于图像。')
    select_ShadowCast = expander_col1.checkbox('纸张阴影', help='模拟纸张表面的阴影效果。')
    select_PageBorder = expander_col2.checkbox('页面边框', help='通过多次堆叠图像来添加页面边框效果。')
    select_Squish = expander_col1.checkbox('挤压', help='通过移除图像的固定水平或垂直部分来创建挤压效果。')
    select_BadPhotoCopy = expander_col1.checkbox('脏复印机', help='使用添加的噪音来产生脏复印机的效果。')
    select_BindingsAndFasteners = expander_col2.checkbox('装订机', help='模拟装订机痕迹')
    # select_pepper = expander_col1.checkbox('pepper', help='在 src 图像上随机散布暗像素。')
    # select_salt = expander_col2.checkbox('salt', help='在 src 图像上随机散布白色像素')
    
    # ink_phase = []
    # paper_phase = []
    # post_phase = []
    phase = []
    
    if select_BadPhotoCopy:
        BadPhotoCopy_params = st.sidebar.expander('脏复印机参数')
        # 噪声类型
        BadPhotoCopy_noise_type_options = {
            '随机': '-1',
            '斑点': '1',
            '高斯': '2',
            '柏林': '3',
            '沃利': '4',
            '矩形图案': '5'
        }
        BadPhotoCopy_noise_type = BadPhotoCopy_params.selectbox(
            "噪声类型",
            list(BadPhotoCopy_noise_type_options.keys()),
            help='生成不同掩模图案的噪声类型'
        )
        
        BadPhotoCopy_noise_side = BadPhotoCopy_params.selectbox(
            "噪声侧",
            ("random", "left", "top", "right", "bottom", "top_left", "top_right", "bottom_left", "bottom_right", "none", "all"),
            help='噪声的位置”。'
        )
        BadPhotoCopy_noise_p = BadPhotoCopy_params.number_input(label='概率', min_value=0.01, max_value=1.00, value=1.00, help='应用此增强的概率。')
        phase.append(BadPhotoCopy(
            noise_type=int(BadPhotoCopy_noise_type_options[BadPhotoCopy_noise_type]),
            noise_side=BadPhotoCopy_noise_side,
            p=float(BadPhotoCopy_noise_p),
        ))
    
    if select_BindingsAndFasteners:
        BindingsAndFasteners_params = st.sidebar.expander('装订机参数')
        BindingsAndFasteners_overlay_types = BindingsAndFasteners_params.selectbox(
            "叠加方法的类型",
            ("random","min","max","mix","normal","lighten","darken","addition","screen","dodge","multiply","divide", "hard_light","grain_merge","overlay",),
            help='叠加方法的类型。'
        )
        BindingsAndFasteners_effect_type = BindingsAndFasteners_params.selectbox(
            "绑定效果类型",
            ("random", "punch_holes", "binding_holes", "clips", "triangle_clips"),
            help='绑定效果类型，可从“随机”、“打孔”、“绑定_孔”、“剪辑”或“三角剪辑”中选择。'
        )
        BindingsAndFasteners_noise_p = BindingsAndFasteners_params.number_input(label='概率', min_value=0.01, max_value=1.00, value=1.00, help='应用此增强的概率。', key='BindingsAndFasteners_noise_p')
        phase.append(BindingsAndFasteners(
            overlay_types = BindingsAndFasteners_overlay_types,
            effect_type = str(BindingsAndFasteners_effect_type),
            p=float(BindingsAndFasteners_noise_p),
        ))
        
    if select_BleedThrough:
        BleedThrough_params = st.sidebar.expander('墨水渗透参数')
        BleedThrough_alpha = BleedThrough_params.number_input(label='强度', min_value=0.1, max_value=1.00, value=0.3, help='渗透效果的强度，推荐值范围为0.1至0.5。', key='BleedThrough_alpha')
        BleedThrough_p = BleedThrough_params.number_input(label='概率', min_value=0.01, max_value=1.00, value=1.00, help='应用此增强的概率。', key='BleedThrough_p')
        
        phase.append(BleedThrough(intensity_range=(0.1, 0.2),
            color_range=(0, 224),
            ksize=(17, 17),
            sigmaX=0,
            alpha=BleedThrough_alpha,
            offsets=(10, 20),
            p = BleedThrough_p
        ))
        
    if select_BrightnessTexturize:
        BrightnessTexturize_params = st.sidebar.expander('纸张纹理参数')
        BrightnessTexturize_p = BrightnessTexturize_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率。', key='BrightnessTexturize_p')
        phase.append(BrightnessTexturize(texturize_range=(0.9, 0.99),
            deviation=0.1,
            p=BrightnessTexturize_p)
        )
        
        
    if select_ColorShift:
        ColorShift_params = st.sidebar.expander('偏移参数')
        ColorShift_offset_x = ColorShift_params.number_input(label='横轴偏移', min_value=0.01, max_value=1.00, value=0.01, help='每个颜色通道时的 x 偏移值', key='ColorShift_offset_x')
        ColorShift_offset_y = ColorShift_params.number_input(label='纵轴偏移', min_value=0.01, max_value=1.00, value=0.01, help='每个颜色通道时的 y 偏移值', key='ColorShift_offset_y')
        ColorShift_p = ColorShift_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率。', key='ColorShift_p')
        
        phase.append(ColorShift(color_shift_offset_x_range = (ColorShift_offset_x,ColorShift_offset_x),
            color_shift_offset_y_range = (ColorShift_offset_y,ColorShift_offset_y),
            color_shift_iterations = (2,3),
            color_shift_brightness_range = (0.9,1.1),
            color_shift_gaussian_kernel_range = (3,3),
            p = ColorShift_p
            )
        )
        
    if select_DirtyDrum:
        DirtyRollers_params = st.sidebar.expander('脏滚筒参数')
        DirtyDrum_line_width = DirtyRollers_params.number_input(label='脏滚筒宽度', min_value=1, max_value=100, value=4, help='脏滚筒宽度', key='DirtyDrum_line_width')
        DirtyDrum_line_concentration = DirtyRollers_params.number_input(label='脏滚筒线的浓度', min_value=0.1, max_value=1.0, value=0.1, help='脏滚筒线的浓度', key='DirtyDrum_line_concentration')
        DirtyDrum_direction_options = {
            '随机': '-1',
            '水平': '0',
            '垂直': '1',
            '两者': '2',
        }
        DirtyDrum_direction = DirtyRollers_params.selectbox(
            "滚筒方向",
            list(DirtyDrum_direction_options.keys()),
            help='效果方向',
            key='DirtyDrum_direction'
        )
        DirtyDrum_noise_intensity = DirtyRollers_params.number_input(label='效果强度', min_value=0.1, max_value=1.0, value=0.5, help='效果强度', key='DirtyDrum_noise_intensity')
        DirtyDrum_p = DirtyRollers_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率。', key='DirtyDrum_p')
        
        phase.append(DirtyDrum(line_width_range=(DirtyDrum_line_width, DirtyDrum_line_width),
            line_concentration=DirtyDrum_line_concentration,
            direction=DirtyDrum_direction_options[DirtyDrum_direction],
            noise_intensity=DirtyDrum_noise_intensity,
            noise_value=(0, 30),
            ksize=(3, 3),
            sigmaX=0,
            p=DirtyDrum_p
        ))
    
    if select_DirtyRollers:
        DirtyRollers_params = st.sidebar.expander('DirtyRollers参数')
        DirtyRollers_p = DirtyRollers_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率。', key='DirtyRollers_p')
        phase.append(DirtyRollers(line_width_range=(12, 25),
            scanline_type=1,
            numba_jit=1,
            p=DirtyRollers_p))
        
    if select_DotMatrix:
        DotMatrix_params = st.sidebar.expander('点阵效果参数')
        DotMatrix_dot_matrix_shape_options = {
            '随机': 'random',
            '圆形':'circle',
            '矩形':'rectangle',
            '三角形':'triangle',
            '菱形': 'diamond'
        }
        DotMatrix_dot_matrix_shape = DotMatrix_params.selectbox(
            "dot_matrix_shape",
            list(DotMatrix_dot_matrix_shape_options.keys()),
            help='点阵效果中单个点的形状。现有的形状有“圆形”、“矩形”、“三角形”和“菱形”。使用“随机”随机选择形状。'
        )
        phase.append(DotMatrix(dot_matrix_shape=DotMatrix_dot_matrix_shape_options[DotMatrix_dot_matrix_shape],
            dot_matrix_dot_width_range=(5, 5),
            dot_matrix_dot_height_range=(5, 5),
            dot_matrix_min_width_range=(1, 1),
            dot_matrix_max_width_range=(50, 50),
            dot_matrix_min_height_range=(1, 1),
            dot_matrix_max_height_range=(50, 50),
            dot_matrix_min_area_range=(10, 10),
            dot_matrix_max_area_range=(800, 800),
            dot_matrix_median_kernel_value_range = (29,29),
            dot_matrix_gaussian_kernel_value_range=(1, 1),
            dot_matrix_rotate_value_range=(0, 0)
        ))
        
    # if select_DoubleExposure:
    #     DoubleExposure_params = st.sidebar.expander('双曝光效果参数')
    #     phase.append(DoubleExposure(gaussian_kernel_range=(9,12),
    #         offset_direction=1,
    #         offset_range=(18,25),
    #     ))

        
    if select_Faxify:
        DoubleExposure_params = st.sidebar.expander('传真效果参数')
        DoubleExposure_monochrome_method  = DoubleExposure_params.selectbox(
            "monochrome_method ",
            ("random", "threshold_li", "threshold_mean", "threshold_otsu", "threshold_sauvola", "threshold_triangle"),
            help='单色阈值方法。'
        )
        DoubleExposure_invert = DoubleExposure_params.checkbox('invert', help='标记以反转半色调效果中的灰度值。')
        phase.append(Faxify(scale_range=(1.0, 1.25),
            monochrome=-1,
            monochrome_method=DoubleExposure_monochrome_method,
            monochrome_arguments={},
            halftone=-1,
            invert=DoubleExposure_invert,
            half_kernel_size=(1, 1),
            angle=(0, 360),
            sigma=(1, 3),
            numba_jit=1,
            p=1))
        
    if select_InkColorSwap:
        InkColorSwap_params = st.sidebar.expander('墨水颜色交换参数')
        InkColorSwap_ink_swap_color = InkColorSwap_params.color_picker('标注', '#F90000')
        phase.append(InkColorSwap(ink_swap_color = (int(InkColorSwap_ink_swap_color[5:7], 16), int(InkColorSwap_ink_swap_color[3:5], 16), int(InkColorSwap_ink_swap_color[1:3], 16)),
            ink_swap_sequence_number_range = (1,10),
            ink_swap_min_width_range=(3,3),
            ink_swap_max_width_range=(100,100),
            ink_swap_min_height_range=(3,3),
            ink_swap_max_height_range=(100,100),
            ink_swap_min_area_range=(10,10),
            ink_swap_max_area_range=(400,400)
            ))
    
    if select_Jpeg:
        Jpeg_params = st.sidebar.expander('JPEG压缩参数')
        Jpeg_p = Jpeg_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率。', key='Jpeg_p')
        phase.append(Jpeg(quality_range=(5, 10), p=Jpeg_p))
    
    if select_LightingGradient:
        LightingGradient_params = st.sidebar.expander('光照渐变参数')
        LightingGradient_direction = LightingGradient_params.slider(label='光照方向', min_value=0, max_value=360, value=90, help='0到360之间的整数，表示灯带的旋转角度。', key='LightingGradient_direction')
        LightingGradient_mode  = LightingGradient_params.selectbox(
            "亮度衰减方式",
            ("gaussian", "linear"),
            help='亮度从最大到最小衰减的方式：线性或高斯。'
        )
        LightingGradient_transparency  = LightingGradient_params.number_input(label='输入图像的透明度', min_value=0.1, max_value=1.0, value=0.5, help='输入图像的透明度', key='LightingGradient_transparency')
        LightingGradient_p = LightingGradient_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='LightingGradient_p')
        
        phase.append(LightingGradient(light_position=None,
            direction=LightingGradient_direction,
            max_brightness=255,
            min_brightness=0,
            mode=LightingGradient_mode,
            transparency=LightingGradient_transparency,
            p=LightingGradient_p
            ))
    if select_LowInkPeriodicLines:
        LowInkPeriodicLines_params = st.sidebar.expander('扫描线参数')
        LowInkPeriodicLines_noise_probability  = LowInkPeriodicLines_params.number_input(label='噪声概率', min_value=0.1, max_value=1.0, value=0.1, help='在生成的线条中添加噪声的概率', key='LowInkPeriodicLines_noise_probability')
        LowInkPeriodicLines_p = LowInkPeriodicLines_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='LowInkPeriodicLines_p')
        
        phase.append(LowInkPeriodicLines(count_range=(2, 5),
            period_range=(10, 30),
            use_consistent_lines=False,
            noise_probability=LowInkPeriodicLines_noise_probability,
            p=LowInkPeriodicLines_p
            ))
        
    if select_Markup:
        Markup_params = st.sidebar.expander('标注参数')
        Mark_num_lines_range  = Markup_params.number_input(label='标注数量', min_value=1, max_value=10, value=2, help='应用此增强的概率', key='Mark_num_lines_range')
        Mark_markup_type_options = {
            '删除线': 'strikethrough',
            '强调':'highlight',
            '下滑线':'underline',
            '交叉':'triangle',
        }
        Mark_markup_type = Markup_params.selectbox(
            "标记样式",
            list(Mark_markup_type_options.keys()),
            help='标记选择“删除线”、“突出显示”、“下划线”或“交叉”。',
            key='Mark_markup_type'
        )
        Mark_markup_ink_options = {
            '随机': 'random',
            '铅笔':'pencil',
            '钢笔':'pen',
            '马克笔':'marker',
            '荧光笔': 'highlighter'
        }
        Mark_markup_ink = Markup_params.selectbox(
            "标注墨水",
            list(Mark_markup_ink_options.keys()),
            help='标记墨水的类型，可以从“随机”、“铅笔”、“钢笔”、“记号笔”或“荧光笔”中进行选择。',
            key='Mark_markup_ink'
        )
        Mark_fillcolor = Markup_params.color_picker('标记颜色', '#FF0000')
        Mark_p = Markup_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='Mark_p')
        
        phase.append(Markup(num_lines_range=(Mark_num_lines_range, Mark_num_lines_range),
            markup_length_range=(0.5, 1),
            markup_thickness_range=(5, 5),
            markup_type=Mark_markup_type_options[Mark_markup_type],
            markup_ink=Mark_markup_ink_options[Mark_markup_ink],
            markup_color=(int(Mark_fillcolor[5:7], 16),int(Mark_fillcolor[3:5], 16),int(Mark_fillcolor[1:3], 16)),
            repetitions=1,
            large_word_mode=1,
            single_word_mode=False,
            p=Mark_p))
    
    if select_NoiseTexturize:
        NoiseTexturize_params = st.sidebar.expander('纸张纹理参数')
        NoiseTexturize_p = NoiseTexturize_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='Mark_p')
        phase.append(NoiseTexturize(sigma_range=(2, 3),
            turbulence_range=(2, 5),
            texture_width_range=(50, 500),
            texture_height_range=(50, 500),
            p=NoiseTexturize_p))
    
    if select_NoisyLines:
        NoisyLines_params = st.sidebar.expander('线条噪声参数')
        NoisyLines_direction_options = {
            '水平': '0',
            '垂直': '1',
            '两者': '2',
            '随机': 'random',
        }
        NoisyLines_direction = NoisyLines_params.selectbox(
            "噪声方向",
            list(NoisyLines_direction_options.keys()),
            help='效果方向',
            key='NoisyLines_direction'
        )
        NoisyLines_p = NoisyLines_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='NoisyLines_p')
        
        phase.append(NoisyLines(noisy_lines_direction = NoisyLines_direction_options[NoisyLines_direction] if NoisyLines_direction_options[NoisyLines_direction]=='random' else int(NoisyLines_direction_options[NoisyLines_direction]),
            noisy_lines_location = "random",
            noisy_lines_number_range = (3,5),
            noisy_lines_color = (0,0,0),
            noisy_lines_thickness_range = (2,2),
            noisy_lines_random_noise_intensity_range = (0.01, 0.1),
            noisy_lines_length_interval_range = (0,100),
            noisy_lines_gaussian_kernel_value_range = (3,3),
            noisy_lines_overlay_method = "ink_to_paper",
            p=NoisyLines_p
            ))
    
    if select_ReflectedLight:
        ReflectedLight_params = st.sidebar.expander('反射光参数')
        ReflectedLight_reflected_light_smoothness  = ReflectedLight_params.number_input(label='平滑度', min_value=0.0, max_value=1.0, value=0.8, help='浮点数决定椭圆的平滑度。该值应在 0 到 1 之间。平滑度值越高，运行速度越慢。', key='ReflectedLight_reflected_light_smoothness')
        ReflectedLight_p = ReflectedLight_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='ReflectedLight_p')
        phase.append(ReflectedLight(reflected_light_smoothness = ReflectedLight_reflected_light_smoothness,
            reflected_light_internal_radius_range=(0.0, 0.2),
            reflected_light_external_radius_range=(0.1, 0.8),
            reflected_light_minor_major_ratio_range = (0.9, 1.0),
            reflected_light_color = (255,255,255),
            reflected_light_internal_max_brightness_range=(0.9,1.0),
            reflected_light_external_max_brightness_range=(0.9,0.9),
            reflected_light_location = "random",
            reflected_light_ellipse_angle_range = (0, 360),
            reflected_light_gaussian_kernel_size_range = (5,310),
            p=ReflectedLight_p
            )
        )
    if select_Scribbles:
        Scribbles_params = st.sidebar.expander('涂鸦参数')
        Scribbles_type_options = {
            '随机': 'random',
            '线条': 'lines',
            '文本': 'text'
        }
        Scribbles_type = Scribbles_params.selectbox(
            "涂鸦类型",
            list(Scribbles_type_options.keys()),
            help='涂鸦类型，可选择“随机”、“线条”或“文本”。',
            key='Scribbles_direction'
        )
        Scribbles_ink_options = {
            '随机': 'random',
            '铅笔': 'pencil',
            '钢笔': 'pen',
            '马克笔': 'marker'
        }
        Scribbles_ink = Scribbles_params.selectbox(
            "涂鸦墨水",
            list(Scribbles_ink_options.keys()),
            help='涂鸦墨水的类型，可以从“随机”、“铅笔”、“钢笔”或“记号笔”中选择。',
            key='Scribbles_ink'
        )
        Scribbles_text = Scribbles_params.text_input('涂鸦文本(默认随机)', 'random', key='Scribbles_text', help='涂鸦文本，仅涂鸦类型为文本时有效')
        Scribbles_p = Scribbles_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='Scribbles_p')
        phase.append(Scribbles(scribbles_type=Scribbles_type_options[Scribbles_type],
            scribbles_ink=Scribbles_ink_options[Scribbles_ink],
            scribbles_location="random",
            scribbles_size_range=(400, 600),
            scribbles_count_range=(1, 6),
            scribbles_thickness_range=(1, 3),
            scribbles_brightness_change=[8, 16],
            scribbles_skeletonize=0,
            scribbles_skeletonize_iterations=(2, 3),
            scribbles_color="random",
            scribbles_text=Scribbles_text,
            scribbles_text_font="random",
            scribbles_text_rotate_range=(0, 360),
            scribbles_lines_stroke_count_range=(1, 6),
            p=Scribbles_p,
            )
        )
        
    if select_ShadowCast:
        ShadowCast_params = st.sidebar.expander('纸张阴影参数')
        ShadowCast_side_options = {
            '随机': 'random',
            '左': 'left',
            '右': 'right',
            '上': 'top',
            '下': 'bottom',
        }
        ShadowCast_side = ShadowCast_params.selectbox(
            "阴影边",
            list(ShadowCast_side_options.keys()),
            help='图像的一侧应用阴影效果。从“随机”、“左”、“右”、“上”或“下”中选择。',
            key='ShadowCast_side'
        )
        ShadowCast_p = ShadowCast_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='ShadowCast_p')
        
        phase.append(ShadowCast(shadow_side = ShadowCast_side_options[ShadowCast_side],
            shadow_vertices_range = (2, 3),
            shadow_width_range=(0.5, 0.8),
            shadow_height_range=(0.5, 0.8),
            shadow_color = (0, 0, 0),
            shadow_opacity_range=(0.5,0.6),
            shadow_iterations_range = (1,2),
            shadow_blur_kernel_range = (101, 301),
            p=ShadowCast_p,
            )
        )
    
    if select_PageBorder:
        PageBorder_params = st.sidebar.expander('页面边框参数')
        PageBorder_page_numbers  = PageBorder_params.number_input(label='页数', min_value=1, max_value=100, value=8, help='确定边框中的页数的整数。', key='PageBorder_page_numbers')
        PageBorder_p = PageBorder_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='PageBorder_p')
        
        phase.append(
            PageBorder(page_border_width_height = (30, -40),
                page_border_color=(0, 0, 0),
                page_border_background_color=(255, 255, 255),
                page_border_use_cache_images = 0,
                page_border_trim_sides = (0, 0, 0, 0),
                page_numbers = PageBorder_page_numbers,
                page_rotate_angle_in_order = 0,
                page_rotation_angle_range = (1, 5),
                curve_frequency=(0, 1),
                curve_height=(1, 2),
                curve_length_one_side=(30, 60),
                same_page_border=0,
                p=PageBorder_p,
            )
        )
        
    if select_Squish:
        Squish_params = st.sidebar.expander('挤压参数')
        Squish_direction_options = {
            '随机': 'random',
            '水平': 0,
            '垂直': 1,
            '两者': 2,
        }
        Squish_direction = Squish_params.selectbox(
            "挤压方向",
            list(Squish_direction_options.keys()),
            help='挤压效果的方向',
            key='Squish_direction'
        )
        Squish_line_options = {
            '随机': 'random',
            '有线条': 1,
            '无线条': 0,
        }
        Squish_line = Squish_params.selectbox(
            "挤压方向",
            list(Squish_line_options.keys()),
            help='是否启用在每个挤压效果中绘制线条。',
            key='Squish_line'
        )
        Squish_p = Squish_params.number_input(label='概率', min_value=0.1, max_value=1.0, value=1.0, help='应用此增强的概率', key='Squish_p')
        
        phase.append(
            Squish(squish_direction = Squish_direction_options[Squish_direction],
                squish_location = "random",
                squish_number_range = (5,10),
                squish_distance_range = (5,7),
                squish_line = Squish_line_options[Squish_line],
                squish_line_thickness_range = (1,1),
                p=Squish_p
                )
        )
    
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
    col2.subheader("特效")
    
    if file is not None:
        # file = os.path.abspath(file)
        image = Image.open(file)
        
        # phase.append(
        #     Squish(squish_direction = 1,
        #         squish_location = "random",
        #         squish_number_range = (5,10),
        #         squish_distance_range = (5,7),
        #         squish_line = "random",
        #         squish_line_thickness_range = (1,1)
        #         )
        # )
        image = pillow_to_opencv(image)
        for one_phase in phase:
            image = one_phase(image)
        image = opencv_to_pillow(image)
        # if len(ink_phase) > 0:
        #     pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase)
        #     image = pillow_to_opencv(image)
        #     image = pipeline(image)
        #     image = opencv_to_pillow(image)
        
        col2.image(image, caption="特效", use_column_width=True)
        download_image(col2, image, "image")
    else:
        col2.info("请上传一张图片")