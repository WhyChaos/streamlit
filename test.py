from augraphy import *
import cv2
import random

ink_phase = [BindingsAndFasteners()]

paper_phase = []

post_phase = []


pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase)


image = cv2.imread("4.jpg")

augmented = pipeline(image)

cv2.imwrite("tmp.png",augmented)