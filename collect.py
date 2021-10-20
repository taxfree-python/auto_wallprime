#import
import os
from random import randint, choice
from time import sleep, time
import re
from PIL import Image,ImageOps
import pyocr
import pyautogui as auto
from collections import defaultdict


class create_data:

    def __init__(self):
        self.check_setting_file()
        global index
        index = self.read_index()
        self.run()


    def __del__(self):
        self.write_index_head(ind)
        print('======================')
        print(f'next_index = {ind + 1}')


    def check_setting_file(self):
        folders = os.scandir()
        for folder in folders:
            if folder.name == 'datum':
                break
        else:
            os.mkdir('datum')
            os.mkdir('datum/images')
            with open('datum/number.txt', mode = 'w') as f:
                f.write('0\n')


    def write_index_head(self, num):
        with open(f'datum/number.txt', mode = 'r+') as f:
            f.write(f'{num} \n')

    def write_index(self, text):
        with open(f'datum/number.txt', mode = 'a') as f:
            f.write(text)

    def read_index(self):
        with open(f'datum/number.txt') as f:
            return int(f.readline())


    def read_num(self, index):
        #global pas
        #start = time()


        tool = pyocr.get_available_tools()[0]

        img = auto.screenshot(region=(175, 490, 480, 225))
        img.save(f'datum/images/image_{index}.png')

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


    def auto_click(self, pos):
        x = [50, 105, 160, 215]
        y = [495, 545, 600, 650]
        r = randint(-8, 8)
        auto.click(x[pos % 4] + r, y[pos // 4] + r)


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
        global ind
        ind = index
        while True:
            start = time()

            ind += 1
            print('--------------------------')
            auto.click(300,600)
            res = self.read_num(ind)
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

            for i in range(16):
                for _ in range(cal[i]):
                    self.auto_click(i)
                    sleep(0.05)
            auto.click(300, 600)

            self.write_index(f'{ind}, {num},\n')

            pass_time = time() - start
            #print(f'index = {ind}, n = {num}, pass_time = {pass_time} ans = {ans[1]}')
            sleep(3.5)

#run
if __name__ == "__create_data__":
    Solver()