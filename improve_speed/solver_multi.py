#import
from random import randint, choice
from time import sleep
import re
from PIL import Image
import pyocr
import pyautogui as auto
import cv2
from multiprocessing import Pool
import numpy as np


class Solver:
    def __init__(self):
        self.run()


    def read_num_multi(self, param):
        tool = pyocr.get_available_tools()[0]

        ret, img = cv2.threshold(param[1], 200, 255, cv2.THRESH_BINARY_INV)
        x_size = img.shape[0]
        y_size = img.shape[1]

        img[168:, :45] = [[255, 255, 255]]
        img[0:, :20] = [[255, 255, 255]]

        #trans = cv2.getRotationMatrix2D((int(x_size / 2), int(y_size / 2)), -3, 0.9)
        #img = cv2.warpAffine(image, trans, (y_size, x_size), borderValue=(255, 255, 255))

        img = Image.fromarray(img)
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = f'{param[0]}', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        if num == 0 or num >= 10**9:
            return (0, (0, [0]))
        else:
            return (num, self.pfactorization(num))


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
        #exception
        if num == 16726708:
            num = 46726708
        if num ==32137965:
            num = 82137965

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
        p = Pool(6)
        for _ in range(10**9):
            img = cv2.cvtColor(np.array(auto.screenshot(region = (175, 490, 470, 225))), cv2.COLOR_RGB2BGR)
            #img.save(f'picture.png')

            langs = [('eng', img), ('snum', img)]
            numbers = p.map(self.read_num_multi, langs)
            pfact = self.check(numbers)

            print(numbers[0][0], numbers[1][0])
            if pfact == 0:
                print('failed pfactorization')
                continue

            for i in range(16):
                for _ in range(pfact[i]):
                    self.auto_click(i)
                    sleep(0.09)
            auto.click(300, 600)

            sleep(3.5)


#run
if __name__ == "__main__":
    Solver()