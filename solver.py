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


    def read_num(self, inputs):
        tool = pyocr.get_available_tools()[0]

        ret, img = cv2.threshold(inputs[1], 180, 255, cv2.THRESH_BINARY_INV)

        img = Image.fromarray(img)
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = f'{inputs[0]}', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        if num == 0 or num >= 10 ** 10:
            return (0, (0, [0]))
        else:
            pfact = self.pfactorization(num)
            if pfact[0] == 0 and num >= 10 ** 8:
                if str(num)[0] == '1':
                    num = int('4' + str(num)[1:])
                elif str(num)[0] == '3':
                    num = int('8' + str(num)[1:])
                elif str(num)[0] == '2':
                    num = int('3' + str(num)[1:])
                elif str(num)[0] == '5':
                    num = int('6' + str(num)[1:])
            if pfact[0] == 0 and str(num)[0] == '7':
                num = int(str(num)[1:])

            return (num, self.pfactorization(num))


    def click(self, pos):
        x = [50, 105, 160, 215]
        y = [495, 545, 600, 650]
        r = randint(-3, 3)
        auto.click(x[pos % 4] + r, y[pos // 4] + r)


    def check(self, numbers):
        status_1 = numbers[0][1][0]
        status_2 =numbers[1][1][0]

        if status_1 == status_2 and status_1 == 1: #both eng and snum succeeded pfact
            length = max(len(str(numbers[0][0])), len(str(numbers[1][0])))
            z = randint(1, 100)
            if length <= 3:
                if z <= 12:
                    return numbers[0][1][1] #return eng
                else:
                    return numbers[1][1][1] #return snum
            elif length <= 6:
                if z <= 68:
                    return numbers[0][1][1] #return eng
                else:
                    return numbers[1][1][1] #return snum
            else:
                if z <= 19:
                    return numbers[0][1][1] #return eng
                else:
                    return numbers[1][1][1] #return snum
        elif status_1 == 1: #eng succeeded pfact
            return numbers[0][1][1]
        elif status_2 == 1: #snum succeeded pfact
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
        p = Pool(6)
        for _ in range(10**9):
            img = cv2.cvtColor(np.array(auto.screenshot(region = (175, 490, 470, 225))), cv2.COLOR_RGB2BGR)

            langs = [('eng', img), ('snum', img)]
            numbers = p.map(self.read_num, langs)
            pfact = self.check(numbers)

            print(numbers[0][0], numbers[1][0])
            if pfact == 0:
                print('failed pfactorization')
                continue

            for i in range(16):
                for _ in range(pfact[i]):
                    self.click(i)
                    sleep(0.07)
            auto.click(300, 600)

            sleep(3.3)


#run
if __name__ == "__main__":
    Solver()
