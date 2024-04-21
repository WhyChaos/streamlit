
from PIL import Image, ImageDraw



from ocr.paddleocr import OCR
from erase.index import erase
from judge.index import Judge
from erase.index import erase



class Rotate:
    def __init__(self):
        pass
    
    def apply(self, image, rotate_angle, rotate_expand, rotate_fillcolor):
        return image.rotate(angle=rotate_angle, expand=(rotate_expand is False), fillcolor=rotate_fillcolor)
        

class Mark:
    def __init__(self, keyword, by_row):
        # ocr，使用paddleocr
        self.orc = OCR.main
        self.judge = Judge(keywords=keyword, by_row=by_row)
        self.keyword = keyword.split()
        
    def apply_mark(self, image, mark_type, mark_color, mark_width):
        if len(self.keyword) == 0:
            return image
        # 关键字判断
        coordinate_word_list = self.orc(image)
        
        coordinate_list = self.judge.main(coordinate_word_list)

        # 标注效果
        if mark_type == '框':
            image = self.apply_frame(img=image, coordinate_list=coordinate_list, mark_color=mark_color, mark_width=mark_width)
        elif mark_type == '斜线':
            image = self.apply_slash(img=image, coordinate_list=coordinate_list, mark_color=mark_color, mark_width=mark_width)
        elif mark_type == '下划线':
            image = self.apply_underline(img=image, coordinate_list=coordinate_list, mark_color=mark_color, mark_width=mark_width)
        elif mark_type == '椭圆':
            image = self.apply_oval(img=image, coordinate_list=coordinate_list, mark_color=mark_color, mark_width=mark_width)
        return image

    def apply_frame(self, img, coordinate_list, mark_color, mark_width):
        for coordinate in coordinate_list:
            x1, y1, x2, y2 = map(int, coordinate)
            draw = ImageDraw.Draw(img)
            draw.line([(x2,y2), (x1,y2)], fill=mark_color, width=mark_width)
            draw.line([(x2,y2), (x2,y1)], fill=mark_color, width=mark_width)
            draw.line([(x1,y1), (x1,y2)], fill=mark_color, width=mark_width)
            draw.line([(x1,y1), (x2,y1)], fill=mark_color, width=mark_width)
            # print(x1, y1, x2, y2)
            # draw.rounded_rectangle([min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2)], radius=5, outline=mark_color, width=mark_width)
        return img
    
    def apply_slash(self, img, coordinate_list, mark_color, mark_width):
        for coordinate in coordinate_list:
            x1, y1, x2, y2 = map(int, coordinate)
            draw = ImageDraw.Draw(img)
            draw.line([(x2,y2), (x1,y1)], fill=mark_color, width=mark_width)
        return img

    def apply_underline(self, img, coordinate_list, mark_color, mark_width):
        for coordinate in coordinate_list:
            x1, y1, x2, y2 = map(int, coordinate)
            draw = ImageDraw.Draw(img)
            draw.line([(x2,y2), (x1,y2)], fill=mark_color, width=mark_width)
        return img
    
    def apply_oval(self, img, coordinate_list, mark_color, mark_width):
        for coordinate in coordinate_list:
            x1, y1, x2, y2 = map(int, coordinate)
            draw = ImageDraw.Draw(img)
            draw.ellipse([(x1,y1), (x2,y2)], outline=mark_color, width=mark_width)
        return img
        
        