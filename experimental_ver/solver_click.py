#import
import os
from random import randint, choice
from time import sleep, time
import re
from PIL import Image,ImageOps
import pyocr
import pyautogui as auto
from collections import defaultdict


class Solver:
    def __init__(self):
        self.run()


    def read_num(self):
        tool = pyocr.get_available_tools()[0]

        img = auto.screenshot(region=(175, 490, 480, 225))

        img = img.point(lambda x: x * 1.2).convert('L').point(lambda x: 0 if x < 230 else x)
        img = ImageOps.invert(img)

        num_eng = re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8)))
        num_snum  = re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8)))

        ans = (int(num_eng or 0), int(num_snum or 0))
        print(ans)

        #pas = time() - start
        if ans[0] == 0 and ans[1] == 0:
            return (0, ans)
        elif ans[0] == 0: #一桁の数字で出やすい
            return (2, ans)
        elif ans[0] == 1 and ans[1] != 1:
            return (2, ans)
        elif ans[0] != ans[1] and ans[0] // 10 == ans[1]:
            return (2, ans)
        elif ans[0] != ans[1]:
            c = choice(list(ans))
            ans = (c, c)
            return (1, ans)
        else:
            return (1, ans)


    def auto_click(self, cal):
        x = [50, 105, 160, 215]
        y = [495, 545, 600, 650]

        for i in range(16):
            for _ in range(cal[i]):
                r = randint(-8, 8)
                auto.click(x[i % 4] + r, y[i // 4] + r)
                sleep(0.05)

        auto.click(300, 600)


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
        while True:
            start = time()

            print('--------------------------')
            auto.click(300,600)
            res = self.read_num()
            num = res[1][res[0] - 1]

            if res[0] == 0:
                print('n = 0, failed recognize')
                continue

            ans = self.pfactorization(num)
            status = ans[0]
            cal = ans[1]

            if status == 0:
                print(f'n = {num}, failed pfactorization')
                sleep(0.1)
                continue

            pass_t = time() - start
            print(pass_t)

            self.auto_click(cal)


            pass_time = time() - start
            print(pass_time)

            sleep(3.5)


#run
if __name__ == "__main__":
    Solver()