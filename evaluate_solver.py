import cv2
import numpy as np
from PIL import Image
from multiprocessing import Pool
from random import randint, choice
import pyocr
import re
import time
import csv

class Measure_solver:
    def measure_solver(self, solver, number):
        spend_time = []

        if number == 1:
            length = 360
        if number == 2:
            length = 991
        if number == 3:
            length = 178

        if solver == 1:
            spend_time.append(time.time())
            p = Pool(6)

            for i in range(length):
                img = cv2.imread(f'data/dataset_{number}/{i}.png')
                langs = [('eng', img), ('snum', img)]

                numbers = p.map(self.read_num_multi, langs)

            spend_time.append(time.time())

            return round(spend_time[1] - spend_time[0], 5)

        if solver == 2 or solver == 3:
            spend_time.append(time.time())
            cnt = 0
            for i in range(length):
                img = cv2.imread(f'data/dataset_{number}/{i}.png')
                numbers = self.read_num(img)

            spend_time.append(time.time())

            return round(spend_time[1] - spend_time[0], 5)



    def read_num_multi(self, val):
        tool = pyocr.get_available_tools()[0]

        ret, img = cv2.threshold(val[1], 180, 255, cv2.THRESH_BINARY_INV)

        img = Image.fromarray(img)
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = f'{val[0]}', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num(self, img):
        tool = pyocr.get_available_tools()[0]

        ret, img = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)

        img = Image.fromarray(img)
        num_eng = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)
        num_snum = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return (num_eng, num_snum)


if __name__ == "__main__":
    for _ in range(100):
        measure = Measure_solver()
        for i in range(1, 3): #solver_number
            for number in range(1, 4): #dataset_number
                t = measure.measure_solver(i, number)
                with open(f'evaluation_solver/solver.csv', 'a') as f:
                    write = csv.writer(f)
                    write.writerow([i, number, t])