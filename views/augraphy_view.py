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
    
# from augraphy import AugraphyPipeline, BadPhotoCopy, BindingsAndFasteners, BleedThrough, Brightness, BrightnessTexturize, ColorPaper, ColorShift, DirtyScreen
from augraphy import *
from utils.pillow_convert_opencv import pillow_to_opencv, opencv_to_pillow


def augraphy_view(file):
    expander = st.sidebar.expander("效果选择")
    expander_col1, expander_col2 = expander.columns(2)
    select_BadPhotoCopy = expander_col1.checkbox('BadPhotoCopy', help='使用添加的噪音来产生脏复印机的效果。')
    select_BindingsAndFasteners = expander_col2.checkbox('BindingsAndFasteners', help='模拟装订机痕迹')
    select_BleedThrough = expander_col1.checkbox('BleedThrough', help='模拟墨水出血和高斯模糊操作组合的渗透效果。')
    select_Brightness = expander_col2.checkbox('Brightness', help='通过选定的倍数调整整个图像的亮度。')
    select_BrightnessTexturize = expander_col1.checkbox('BrightnessTexturize', help='在亮度通道中创建随机噪声以模拟纸张纹理。')
    select_ColorPaper = expander_col2.checkbox('ColorPaper', help='根据用户输入的色调和饱和度更改输入纸张的颜色。')
    select_ColorShift = expander_col1.checkbox('ColorShift', help='将每个 BGR 颜色通道移动一定的偏移量以创建移动的颜色效果。')
    # select_DepthSimulatedBlur = expander_col2.checkbox('DepthSimulatedBlur', help='通过模糊图像的小椭圆区域，创建相机的深度模拟模糊效果。')
    select_DirtyRollers = expander_col2.checkbox('DirtyRollers', help='模拟某些文档扫描仪创建的效果')
    select_DotMatrix = expander_col1.checkbox('DotMatrix', help='通过在检测到的轮廓中绘制平均颜色的点来创建点阵效果。')
    select_Faxify = expander_col2.checkbox('Faxify', help='模拟图像中的传真效果。')
    select_Gamma = expander_col1.checkbox('Gamma', help='通过选定的乘数调整整个图像的伽玛值')
    
    
    # select_pepper = expander_col1.checkbox('pepper', help='在 src 图像上随机散布暗像素。')
    # select_salt = expander_col2.checkbox('salt', help='在 src 图像上随机散布白色像素')
    
    ink_phase = []
    paper_phase = []
    post_phase = []
    
    if select_BadPhotoCopy:
        BadPhotoCopy_params = st.sidebar.expander('BadPhotoCopy参数')
        BadPhotoCopy_noise_type = BadPhotoCopy_params.selectbox(
            "noise_type",
            ("-1", "1", "2", "3", "4", "5"),
            help='生成不同掩模图案的噪声类型。 使用-1 随机选择。 1 = sklearn.datasets 的 make_blobs 噪声 2 = 高斯噪声 3 = perlin 噪声 4 = worley 噪声 5 = 矩形图案噪声'
        )
        
        BadPhotoCopy_noise_side = BadPhotoCopy_params.selectbox(
            "noise_side",
            ("random", "left", "top", "right", "bottom", "top_left", "top_right", "bottom_left", "bottom_right", "none", "all"),
            help='噪声的位置。 选择：“随机”、“左”、“上”、“右”、“下”、“左上”、“右上”、“左下”、“右下”、“无”、“全部”。'
        )
        BadPhotoCopy_noise_iteration = BadPhotoCopy_params.container()
        BadPhotoCopy_noise_iteration.write('noise_iteration')
        BadPhotoCopy_noise_iteration_columns = BadPhotoCopy_noise_iteration.columns(2)
        BadPhotoCopy_noise_iteration_x = BadPhotoCopy_noise_iteration_columns[0].number_input(label='x', min_value=0, max_value=100, value=2, help='用于确定在掩码中应用噪声的迭代次数的整数对。')
        BadPhotoCopy_noise_iteration_y = BadPhotoCopy_noise_iteration_columns[1].number_input(label='y', min_value=0, max_value=100, value=3, help='用于确定在掩码中应用噪声的迭代次数的整数对。')
        
        BadPhotoCopy_noise_size = BadPhotoCopy_params.container()
        BadPhotoCopy_noise_size.write('noise_size')
        BadPhotoCopy_noise_size_columns = BadPhotoCopy_noise_size.columns(2)
        BadPhotoCopy_noise_size_x = BadPhotoCopy_noise_size_columns[0].number_input(label='x', min_value=0, max_value=100, value=2, help='用于确定掩模中噪声规模的一对整数')
        BadPhotoCopy_noise_size_y = BadPhotoCopy_noise_size_columns[1].number_input(label='y', min_value=0, max_value=100, value=3, help='用于确定掩模中噪声规模的一对整数')
        
        BadPhotoCopy_noise_value = BadPhotoCopy_params.container()
        BadPhotoCopy_noise_value.write('noise_value')
        BadPhotoCopy_noise_value_columns = BadPhotoCopy_noise_value.columns(2)
        BadPhotoCopy_noise_value_x = BadPhotoCopy_noise_value_columns[0].number_input(label='x', min_value=1, max_value=1000, value=32, help='噪声的强度范围，值越低，效果越暗。')
        BadPhotoCopy_noise_value_y = BadPhotoCopy_noise_value_columns[1].number_input(label='y', min_value=1, max_value=1000, value=128, help='噪声的强度范围，值越低，效果越暗。')
        
        BadPhotoCopy_noise_sparsity = BadPhotoCopy_params.container()
        BadPhotoCopy_noise_sparsity.write('noise_sparsity')
        BadPhotoCopy_noise_sparsity_columns = BadPhotoCopy_noise_sparsity.columns(2)
        BadPhotoCopy_noise_sparsity_columns_x = BadPhotoCopy_noise_sparsity_columns[0].number_input(label='x', min_value=0.00, max_value=1.00, value=0.15, help='一对确定噪声稀疏度的浮子')
        BadPhotoCopy_noise_sparsity_columns_y = BadPhotoCopy_noise_sparsity_columns[1].number_input(label='y', min_value=0.00, max_value=1.00, value=0.15, help='一对确定噪声稀疏度的浮子')
        
        BadPhotoCopy_noise_concentration = BadPhotoCopy_params.container()
        BadPhotoCopy_noise_concentration.write('noise_concentration')
        BadPhotoCopy_noise_concentration_columns = BadPhotoCopy_noise_concentration.columns(2)
        BadPhotoCopy_noise_concentration_columns_x = BadPhotoCopy_noise_concentration_columns[0].number_input(label='x', min_value=0.00, max_value=1.00, value=0.30, help='一对确定噪声浓度的浮子。')
        BadPhotoCopy_noise_concentration_columns_y = BadPhotoCopy_noise_concentration_columns[1].number_input(label='y', min_value=0.00, max_value=1.00, value=0.30, help='一对确定噪声浓度的浮子。')
        
        BadPhotoCopy_blur_noise = BadPhotoCopy_params.selectbox(
            "blur_noise",
            ("-1", "0", "1"),
            help='标记以启用噪声掩模中的模糊。 使用-1随机选择'
        )
        BadPhotoCopy_blur_noise_kernel = BadPhotoCopy_params.container()
        BadPhotoCopy_blur_noise_kernel.write('blur_noise_kernel')
        BadPhotoCopy_blur_noise_kernel_columns = BadPhotoCopy_blur_noise_kernel.columns(2)
        BadPhotoCopy_blur_noise_kernel_columns_x = BadPhotoCopy_blur_noise_kernel_columns[0].number_input(label='x', min_value=1, max_value=100, value=5, help='模糊噪声掩模的内核。')
        BadPhotoCopy_blur_noise_kernel_columns_y = BadPhotoCopy_blur_noise_kernel_columns[1].number_input(label='y', min_value=1, max_value=100, value=5, help='模糊噪声掩模的内核。')
        
        BadPhotoCopy_wave_pattern = BadPhotoCopy_params.selectbox(
            "wave_pattern",
            ("-1", "0", "1"),
            help='启用噪声中的波形。 使用-1 随机选择。'
        )
        
        BadPhotoCopy_edge_effect = BadPhotoCopy_params.selectbox(
            "edge_effect",
            ("-1", "0", "1"),
            help='将sobel边缘效果添加到噪声掩模中。 使用-1 随机选择。'
        )
        
        BadPhotoCopy_noise_p = BadPhotoCopy_params.number_input(label='p', min_value=0.01, max_value=1.00, value=1.00, help='应用此增强的概率。')
       
        
        ink_phase.append(BadPhotoCopy(
            noise_type=int(BadPhotoCopy_noise_type),
            noise_side=BadPhotoCopy_noise_side,
            noise_iteration=(int(BadPhotoCopy_noise_iteration_x),int(BadPhotoCopy_noise_iteration_y)),
            noise_size=(int(BadPhotoCopy_noise_size_x),int(BadPhotoCopy_noise_size_y)),
            noise_value=(int(BadPhotoCopy_noise_value_x),int(BadPhotoCopy_noise_value_y)),
            noise_sparsity=(float(BadPhotoCopy_noise_sparsity_columns_x),float(BadPhotoCopy_noise_sparsity_columns_y)),
            noise_concentration=(float(BadPhotoCopy_noise_concentration_columns_x),float(BadPhotoCopy_noise_concentration_columns_y)),
            blur_noise=int(BadPhotoCopy_blur_noise),
            blur_noise_kernel=(int(BadPhotoCopy_blur_noise_kernel_columns_x), int(BadPhotoCopy_blur_noise_kernel_columns_y)),
            wave_pattern=int(BadPhotoCopy_wave_pattern),
            edge_effect=int(BadPhotoCopy_edge_effect),
            p = float(BadPhotoCopy_noise_p),
        ))
    
    if select_BindingsAndFasteners:
        BindingsAndFasteners_params = st.sidebar.expander('BindingsAndFasteners参数')
        BindingsAndFasteners_overlay_types = BindingsAndFasteners_params.selectbox(
            "overlay_types",
            ("random","min","max","mix","normal","lighten","darken","addition","screen","dodge","multiply","divide", "hard_light","grain_merge","overlay",),
            help='叠加方法的类型。'
        )
        BindingsAndFasteners_foreground = BindingsAndFasteners_params.file_uploader("上传前景图像（默认无）", type=["jpg", "jpeg", "png"])
        BindingsAndFasteners_effect_type = BindingsAndFasteners_params.selectbox(
            "effect_type",
            ("random", "punch_holes", "binding_holes", "clips", "triangle_clips"),
            help='绑定效果类型，可从“随机”、“打孔”、“绑定_孔”、“剪辑”或“三角剪辑”中选择。'
        )
        ink_phase.append(BindingsAndFasteners(
            overlay_types = BindingsAndFasteners_overlay_types,
            foreground = str(BindingsAndFasteners_foreground),
            effect_type = str(BindingsAndFasteners_effect_type),
            
        ))
        
    if select_BleedThrough:
        BleedThrough_params = st.sidebar.expander('BleedThrough参数')
        BleedThrough_blur_noise_kernel_columns = BleedThrough_params.columns(2)
        BleedThrough_blur_noise_kernel_columns_x = BleedThrough_blur_noise_kernel_columns[0].number_input(label='x', min_value=1, max_value=99, value=17, step=2, help='用于对内核大小进行采样的高度/宽度对的元组。较高的值会增加出血效果的扩散。')
        BleedThrough_blur_noise_kernel_columns_y = BleedThrough_blur_noise_kernel_columns[1].number_input(label='y', min_value=1, max_value=99, value=17, step=2, help='用于对内核大小进行采样的高度/宽度对的元组。较高的值会增加出血效果的扩散。')
        BleedThrough_alpha = BleedThrough_params.number_input(label='alpha', min_value=0.1, max_value=0.9, value=0.2, step=0.1, help='出血效果的强度，推荐值范围为0.1至0.5。')
        ink_phase.append(BleedThrough(
            intensity_range=(0.1, 0.9),
            color_range=(0, 224),
            ksize=(int(BleedThrough_blur_noise_kernel_columns_x), int(BleedThrough_blur_noise_kernel_columns_y)),
            sigmaX=1,
            alpha=BleedThrough_alpha,
            offsets=(20, 20),
            p=1)
        )
        
    if select_Brightness:
        Brightness_params = st.sidebar.expander('Brightness参数')
        Brightness_columns = Brightness_params.columns(2)
        Brightness_min_brightness = Brightness_columns[0].checkbox('min_brightness ', help='标记以在增强图像中启用最小亮度强度值。')
        Brightness_numba_jit = Brightness_columns[1].checkbox('numba_jit ', help='该标志启用 numba jit 来加速增强中的处理')
        ink_phase.append(Brightness(brightness_range=(0.8, 1.4),
                                    min_brightness=Brightness_min_brightness,
                                    min_brightness_value=(20, 50),
                                    numba_jit=Brightness_numba_jit, 
                                    p=1)
                        )
        
    if select_BrightnessTexturize:
        BrightnessTexturize_params = st.sidebar.expander('BrightnessTexturize参数')
        BrightnessTexturize_texturize_range_columns = BrightnessTexturize_params.columns(2)
        BrightnessTexturize_texturize_range_columns_x = BrightnessTexturize_texturize_range_columns[0].number_input(label='x', min_value=0.01, max_value=10.00, value=0.8, help='一对浮点确定亮度矩阵采样值的范围。建议值 = <1/宽度对的元组。较高的值会增加出血效果的扩散。')
        BrightnessTexturize_texturize_range_columns_y = BrightnessTexturize_texturize_range_columns[1].number_input(label='y', min_value=0.01, max_value=10.00, value=0.99, help='一对浮点确定亮度矩阵采样值的范围。建议值 = <1/宽度对的元组。较高的值会增加出血效果的扩散。')
        BrightnessTexturize_deviation = BrightnessTexturize_params.number_input(label='deviation', min_value=0.01, max_value=10.00, value=0.08, help='均匀样品的额外变化。')
        ink_phase.append(BrightnessTexturize(texturize_range=(BrightnessTexturize_texturize_range_columns_x, BrightnessTexturize_texturize_range_columns_y),
                                            deviation=BrightnessTexturize_deviation,
                                            p=1)
                        )
        
    if select_ColorPaper:
        ColorPaper_params = st.sidebar.expander('ColorPaper参数')
         
        BrightnessTexturize_hue_range_columns = ColorPaper_params.columns(2)
        BrightnessTexturize_hue_range_columns_x = BrightnessTexturize_hue_range_columns[0].number_input(label='x', min_value=1, max_value=1000, value=28, help='确定色调值采样范围的整数对。')
        BrightnessTexturize_hue_range_columns_y = BrightnessTexturize_hue_range_columns[1].number_input(label='y', min_value=1, max_value=1000, value=45, help='确定色调值采样范围的整数对。')
        BrightnessTexturize_saturation_range_columns = ColorPaper_params.columns(2)
        BrightnessTexturize_saturation_range_columns_x = BrightnessTexturize_saturation_range_columns[0].number_input(label='x', min_value=1, max_value=1000, value=10, help='确定饱和度值采样范围的整数对。')
        BrightnessTexturize_saturation_range_columns_y = BrightnessTexturize_saturation_range_columns[1].number_input(label='y', min_value=1, max_value=1000, value=40, help='确定饱和度值采样范围的整数对。')
        ink_phase.append(ColorPaper(hue_range=(int(BrightnessTexturize_hue_range_columns_x), int(BrightnessTexturize_hue_range_columns_y)),
                                    saturation_range=(int(BrightnessTexturize_saturation_range_columns_x), int(BrightnessTexturize_saturation_range_columns_y)),
                                    p=1)
                        )
        
    
        
    if select_ColorShift:
        ColorShift_params = st.sidebar.expander('ColorShift参数')
        BrightnessTexturize_color_shift_offset_x_range_columns = ColorShift_params.columns(2)
        BrightnessTexturize_color_shift_offset_x_range_columns_x = BrightnessTexturize_color_shift_offset_x_range_columns[0].number_input(label='x', min_value=1, max_value=1000, value=3, help='一对整数/浮点数确定移动每个颜色通道时的 x 偏移值。 如果值在 0.0 到 1.0 范围内且值为 float，则 x 偏移量将按图像宽度缩放： x 偏移量 (int) = 图像宽度 * x 偏移量（float 和 0.0 - 1.0）')
        BrightnessTexturize_color_shift_offset_x_range_columns_y = BrightnessTexturize_color_shift_offset_x_range_columns[1].number_input(label='y', min_value=1, max_value=1000, value=5, help='一对整数/浮点数确定移动每个颜色通道时的 x 偏移值。 如果值在 0.0 到 1.0 范围内且值为 float，则 x 偏移量将按图像宽度缩放： x 偏移量 (int) = 图像宽度 * x 偏移量（float 和 0.0 - 1.0）')
        BrightnessTexturize_color_shift_offset_y_range_columns = ColorShift_params.columns(2)
        BrightnessTexturize_color_shift_offset_y_range_columns_x = BrightnessTexturize_color_shift_offset_y_range_columns[0].number_input(label='x', min_value=1, max_value=1000, value=3, help='一对整数/浮点数确定移动每个颜色通道时的 y 偏移值。 如果值在 0.0 到 1.0 范围内且值为 float，则 y 偏移量将按图像高度缩放： y 偏移量 (int) = 图像高度 * y 偏移量（float 和 0.0 - 1.0）')
        BrightnessTexturize_color_shift_offset_y_range_columns_y = BrightnessTexturize_color_shift_offset_y_range_columns[1].number_input(label='y', min_value=1, max_value=1000, value=5, help='一对整数/浮点数确定移动每个颜色通道时的 y 偏移值。 如果值在 0.0 到 1.0 范围内且值为 float，则 y 偏移量将按图像高度缩放： y 偏移量 (int) = 图像高度 * y 偏移量（float 和 0.0 - 1.0）')
        
        ink_phase.append(ColorShift(color_shift_offset_x_range=(int(BrightnessTexturize_color_shift_offset_x_range_columns_x), int(BrightnessTexturize_color_shift_offset_x_range_columns_y)),
                                    color_shift_offset_y_range=(int(BrightnessTexturize_color_shift_offset_y_range_columns_x), int(BrightnessTexturize_color_shift_offset_y_range_columns_y)),
                                    color_shift_iterations=(2, 3),
                                    color_shift_brightness_range=(0.9, 1.1),
                                    color_shift_gaussian_kernel_range=(3, 3),
                                    p=1)
                        )
    
    if select_DirtyRollers:
        DirtyRollers_params = st.sidebar.expander('DirtyRollers参数')
        DirtyRollers_line_width_range_columns = DirtyRollers_params.columns(2)
        DirtyRollers_line_width_range_columns_x = DirtyRollers_line_width_range_columns[0].number_input(label='min', min_value=1, max_value=1000, value=8, help='确定范围的整数对脏滚筒线的宽度进行采样')
        DirtyRollers_line_width_range_columns_y = DirtyRollers_line_width_range_columns[1].number_input(label='max', min_value=1, max_value=1000, value=8, help='确定范围的整数对脏滚筒线的宽度进行采样')

        ink_phase.append(DirtyRollers(line_width_range=(int(DirtyRollers_line_width_range_columns_x), int(DirtyRollers_line_width_range_columns_y)),
                                    scanline_type=0,
                                    numba_jit=1,
                                    p=1))
        
    if select_DotMatrix:
        DotMatrix_params = st.sidebar.expander('DotMatrix参数')
        DotMatrix_dot_matrix_shape = DotMatrix_params.selectbox(
            "dot_matrix_shape",
            ("random", "circle", "rectangle", "triangle", "diamond"),
            help='点阵效果中单个点的形状。现有的形状有“圆形”、“矩形”、“三角形”和“菱形”。使用“随机”随机选择形状。'
        )
        ink_phase.append(DotMatrix(dot_matrix_shape=DotMatrix_dot_matrix_shape, 
                                   dot_matrix_dot_width_range=(3, 19),
                                   dot_matrix_dot_height_range=(3, 19),
                                   dot_matrix_min_width_range=(1, 2),
                                   dot_matrix_max_width_range=(150, 200), 
                                   dot_matrix_min_height_range=(1, 2), 
                                   dot_matrix_max_height_range=(150, 200), 
                                   dot_matrix_min_area_range=(10, 20), 
                                   dot_matrix_max_area_range=(2000, 5000),
                                   dot_matrix_median_kernel_value_range=(128, 255),
                                   dot_matrix_gaussian_kernel_value_range=(1, 3), 
                                   dot_matrix_rotate_value_range=(0, 360), 
                                   numba_jit=1, 
                                   p=1))
        
    if select_Faxify:
        DoubleExposure_params = st.sidebar.expander('Faxify参数')
        DoubleExposure_monochrome_method  = DoubleExposure_params.selectbox(
            "monochrome_method ",
            ("random", "threshold_li", "threshold_mean", "threshold_otsu", "threshold_sauvola", "threshold_triangle"),
            help='单色阈值方法。'
        )
        DoubleExposure_invert = DoubleExposure_params.checkbox('invert', help='标记以反转半色调效果中的灰度值。')
        ink_phase.append(Faxify(scale_range=(1.0, 1.25),
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
        
    if select_Gamma:
        Gamma_params = st.sidebar.expander('Gamma参数')
        DirtyRollers_Gamma_columns = Gamma_params.columns(2)
        DirtyRollers_Gamma_columns_x = DirtyRollers_Gamma_columns[0].number_input(label='min', min_value=0.1, max_value=100.0, value=0.5, help='一对整数，确定伽玛偏移采样的范围。')
        DirtyRollers_Gamma_columns_y = DirtyRollers_Gamma_columns[1].number_input(label='max', min_value=0.1, max_value=100.0, value=1.5, help='一对整数，确定伽玛偏移采样的范围。')

        ink_phase.append(Gamma(gamma_range=(DirtyRollers_Gamma_columns_x, DirtyRollers_Gamma_columns_y), p=1))
    
    
    

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
    col2.subheader("augraphy效果")
    
    if file is not None:
        # file = os.path.abspath(file)
        image = Image.open(file)
        
        # 处理图片=
        opera = Opera(keyword, keyword_state)
        image = opera.main(image, keyword_type)
        
        if len(ink_phase) > 0:
            pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase)
            image = pillow_to_opencv(image)
            image = pipeline(image)
            image = opencv_to_pillow(image)
            
        
        col2.image(image, caption="augraphy效果", use_column_width=True)
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