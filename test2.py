from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, lang="ch")
image = Image.open('./1.jpg')
image_np = np.array(image)
result = ocr.ocr(image_np, cls=True)

for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line[1][0])