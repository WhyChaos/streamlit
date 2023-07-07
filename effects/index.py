
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import random
import numpy as np
import math
from effects.scan_effect import ScanEffect
from effects.photo_effect import PhotoEffect


class Effect:
    def __init__(self, type='scan'):
        if type == 'scan':
            self.effect = ScanEffect()
        elif type == 'photo':
            self.effect = PhotoEffect()

    def main(self, image):
        return self.effect.main(image)
