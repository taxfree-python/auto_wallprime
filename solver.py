#import
from random import randint
from time import sleep
import re
from PIL import Image,ImageOps,ImageFilter
import PIL
import pyocr
import pyautogui as auto




class solver:

    def read_num(self, flag):
        tool = pyocr.get_available_tools()[0]

        img = auto.screenshot(region=(173, 490, 480, 225))

        img = img.point(lambda x: x * 1.2).convert('L').point(lambda x: 0 if x < 230 else x)
        img = ImageOps.invert(img)

        num_eng = re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8)))
        num_snum  = re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8)))


        print(num_eng, num_snum)
        if flag:
            return int(num_snum)

        if num_eng == '' and num_snum == '':
            return 0
        elif num_eng == '': #num_engが空，一桁の数字で出やすい
            return int(num_snum)
        elif num_eng == '': #下の処理で，index_errorが出ないようにするため
            return int(num_eng)
        elif num_eng == 1 and num_snum != 1: #num_engで1が出た，かつ，num_snumは1じゃない
            return int(num_snum)
        elif num_eng != num_snum and num_eng[:-1] == num_snum:
            return int(num_snum)
        else:
            return int(num_eng)

    def auto_click(self, cal):
        x = [50, 105, 160, 215]
        y = [495, 545, 600, 650]
        r = randint(-8, 8)
        auto.click(x[cal%4] + r, y[cal//4] + r)


    def factorization(self, num):
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
        cnt = 0
        flag = False
        while True:
            print('--------------------------')
            auto.click(300,600)
            num = self.read_num(flag)

            if num == 0:
                print('n = 0, failed recognize')
                flag = True
                sleep(0.1)
                continue

            ans = self.factorization(num)

            if ans[0] == 0:
                print(f'n = {num}, failed factorization')
                flag = True
                sleep(0.1)
                continue

            flag = False
            for i in range(16):
                for _ in range(ans[1][i]):
                    self.auto_click(i)
                    sleep(0.03)
            sleep(0.05)
            auto.click(300, 600)

            print(f'number = {num}')
            sleep(3.7)

#run
solve = solver()
solve.run()
