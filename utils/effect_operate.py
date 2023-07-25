import sys
sys.path.append('../')

from PIL import Image
from main2 import Opera
from effects.scan_effect import ScanEffect
from effects.photo_screen_effect import PhotoScreenEffect
from effects.screen_effect import ScreenEffect
from effects.photo_effect import PhotoEffect
from utils.convert_gray import convert_gray

def main(data_json, image):
    if data_json['option'] == '扫描':
        return scan_effect_operate(data_json, image)
    elif data_json['option'] == '拍照':
        return photo_effect_operate(data_json, image)
    elif data_json['option'] == '拍照（屏幕)':
        return photo_screen_effect_operate(data_json, image)
    elif data_json['option'] == '屏幕':
        return screen_effect_operate(data_json, image)
    else:
        raise ValueError("")

def scan_effect_operate(data_json, image):
    # 处理图片=
    opera = Opera(data_json['keyword'], data_json['keyword_state'])
    image = opera.main(image, data_json['keyword_type'])
    
    if data_json['is_gray']:
        image = convert_gray(image)
    
    effect = ScanEffect()
    if data_json['scan_line_probability'] > 0:
        image = effect.apply_scan_line_effect(image=image, probability=data_json['scan_line_probability']/100.0, black_probability=data_json['black_scan_line_probability']/100.0)
    if data_json['noise_probability'] > 0:
        image = effect.apply_scan_noise_effect(image=image, probability=data_json['noise_probability']/1000.0, black_probability=data_json['black_noise_probability']/100.0)
    image = effect.apply_scan_brightness_effect(image=image, factor=data_json['brightness_factor']/10.0)
    image = effect.apply_scan_contrast_effect(image=image, factor=data_json['contrast_factor']/10.0)
    if data_json['curve_effect'] != '纸张平整':
        image = effect.apply_scan_curve_effect(image=image, type=int(data_json['curve_effect'][-1]))
    return image
    

def screen_effect_operate(data_json, image):
    # 处理图片=
    opera = Opera(data_json['keyword'], data_json['keyword_state'])
    image = opera.main(image, data_json['keyword_type'])
    
    #灰度
    if data_json['is_gray']:
        image = convert_gray(image)
    # if background_type == '随机':
    effect = ScreenEffect()
    image = effect.main(image, data_json['moier_weight'], data_json['moier_type'], data_json['light_weight'])
    return image

def photo_effect_operate(data_json, image):
    # 处理图片=
    opera = Opera(data_json['keyword'], data_json['keyword_state'])
    image = opera.main(image, data_json['keyword_type'])
    #灰度
    if data_json['is_gray']:
        image = convert_gray(image)
    
    effect = PhotoEffect()
    image = effect.main(image=image)
    return image

def photo_screen_effect_operate(data_json, image):
    # 处理图片=
    opera = Opera(data_json['keyword'], data_json['keyword_state'])
    image = opera.main(image, data_json['keyword_type'])
    #灰度
    if data_json['is_gray']:
        image = convert_gray(image)
    
    effect = PhotoScreenEffect()
    image = effect.main(image=image)
    return image