#import
from random import randint, choice
from time import sleep
import re
from PIL import Image
import pyocr
import pyautogui as auto
import cv2
import numpy as np


class Solver:
    def __init__(self):
        self.run()


    def read_num(self):
        tool = pyocr.get_available_tools()[0]

        img = cv2.cvtColor(np.array(auto.screenshot(region = (175, 490, 470, 225))), cv2.COLOR_RGB2BGR)

        ret, img = cv2.threshold(img, 170, 255, cv2.THRESH_BINARY_INV)

        img[165:, :45] = [[255, 255, 255]]
        img[0:, :20] = [[255, 255, 255]]
        img = Image.fromarray(img)

        num_eng = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)
        num_snum  = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        if num_eng == 0 or num_eng >= 10**9:
            if num_snum == 0 or num_snum >= 10**9:
                return [(0, (0, [0])), (0, (0, [0]))]
            else:
                return [(0, (0, [0])), (num_snum, self.pfactorization(num_snum))]
        else:
            if num_snum == 0 or num_snum >= 10**9:
                return [(num_eng, self.pfactorization(num_eng)), (0, (0, [0]))]
            else:
                return [(num_eng, self.pfactorization(num_eng)), (num_snum, self.pfactorization(num_snum))]


    def auto_click(self, pfact):
        x = [50, 105, 160, 215]
        y = [495, 545, 600, 650]
        r = randint(-3, 3)
        auto.click(x[pfact % 4] + r, y[pfact // 4] + r)


    def check(self, numbers):
        status_1 = numbers[0][1][0]
        status_2 =numbers[1][1][0]

        if status_1 == status_2 and status_1 == 1:
            return choice((numbers[0][1][1], numbers[1][1][1], numbers[1][1][1]))
        if status_1 == 1:
            return numbers[0][1][1]
        if status_2 == 1:
            return numbers[1][1][1]
        else:
            return 0


    def pfactorization(self, num):
        fact = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
        cal = []
        for f in fact:
            cnt = 0
            while num % f == 0:
                cnt += 1
                num //= f

            cal.append(cnt)

        if num == 1:
            return (1, cal)
        else:
            return (0, cal)


    def run(self):
        for _ in range(10**9):
            numbers = self.read_num()
            pfact = self.check(numbers)

            print(numbers[0][0], numbers[1][0])
            if pfact == 0:
                print('failed pfactorization')
                continue

            for i in range(16):
                for _ in range(pfact[i]):
                    self.auto_click(i)
                    sleep(0.10)
            auto.click(300, 600)

            sleep(4.0)


#run
if __name__ == "__main__":
    Solver()