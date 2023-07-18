import os
import math


class Judge:
    def __init__(self, keywords, by_row=True):
        self.by_row = by_row
        self.keywords = keywords.split()

    def main(self, coordinate_word_list):
        coordinate_list = []
        for coordinate_word in coordinate_word_list:
            for keyword in self.keywords:
                # 判断是否为关键字
                if keyword in coordinate_word['word']:
                    if self.by_row:
                        coordinate_list.append(coordinate_word['coordinate'])
                    else:
                        position_list = self.find(
                            keyword, coordinate_word['word'])
                        if len(position_list) != 0:
                            x1, y1, x2, y2 = map(
                                int, coordinate_word['coordinate'])
                            for position in position_list:
                                tmp = (x2-x1)/len(coordinate_word['word'])
                                coordinate_list.append(
                                    [math.floor(x1+tmp*(position-1)), y1, math.floor(x1+tmp*(position+len(keyword))), y2])

        return coordinate_list

    def find(self, keyword, sentence):
        position_list = []
        start_position = 0
        while True:
            position = sentence.find(keyword, start_position)
            if position == -1:
                break
            position_list.append(position)
            start_position = position + 1

        return position_list
