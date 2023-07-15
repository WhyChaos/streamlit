from ocr.paddleocr import OCR
from erase.index import erase
from judge.index import Judge
from erase.index import erase
import streamlit as st


class Opera:
    def __init__(self, keyword):
        # ocr，使用paddleocr
        self.orc = OCR.main
        self.judge = Judge(keyword)
        self.keyword = keyword.split()
        
    def main(self, image, keyword_type):
        if len(self.keyword) == 0:
            return image
        # 关键字判断
        coordinate_word_list = self.orc(image)
        
        coordinate_list = []
        for coordinate_word in coordinate_word_list:
            # 判断是否为关键字
            if (self.judge.main(coordinate_word['word'])):
                print(coordinate_word['word'])
                coordinate_list.append(coordinate_word['coordinate'])
        # 抹去关键字信息，马赛克或全黑效果 type='dark'|type='mosaic'
        if keyword_type == '马赛克':
            image = erase(image=image, coordinate_list=coordinate_list)
        else:
            image = erase(image=image, coordinate_list=coordinate_list, type='dark')
        
        return image