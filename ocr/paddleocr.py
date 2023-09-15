from paddleocr import PaddleOCR, draw_ocr
import numpy as np

class OCR:
    def __init__(self):
        pass

    @staticmethod
    def main(image):
        image_np = np.array(image)
        # ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        ocr = PaddleOCR(use_angle_cls=True,lang="ch",
            rec_model_dir='./models/ch_PP-OCRv3_rec_slim_infer/',
            cls_model_dir='./models/ch_ppocr_mobile_v2.0_cls_slim_infer/',
            det_model_dir='./models/ch_PP-OCRv3_det_slim_infer/')

        result = ocr.ocr(image_np, cls=True)

        coordinate_word_list = []

        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                coordinate_word_list.append(
                    {'word': line[1][0], 'coordinate': (line[0][0][0], line[0][0][1], line[0][2][0], line[0][2][1])})
        return coordinate_word_list
