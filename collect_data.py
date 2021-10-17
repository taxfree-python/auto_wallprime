#import
import os
from random import randint
from time import sleep
import re
from PIL import Image,ImageOps,ImageFilter
import pyocr
import pyautogui as auto


class create_data:

    def __init__(self):
        global file_index
        self.check_setting_file()
        file_index = self.search_file_number()
        self.make_folder()
        self.run()


    def __del__(self):
        #m = self.search_file_number(1)
        print('======================')
        print(f'next_number = {file_index + 1}')
        self.write_setting(file_index + 1)


    def check_setting_file(self):
        folders = os.scandir()
        for folder in folders:
            if folder.name == 'datum':
                break
        else:
            os.mkdir('datum')

        files = os.scandir('datum')
        for file in files:
            if file.name == 'setting.txt':
                break
        else:
            with open('datum/setting.txt', mode = 'w') as f:
                f.write('0')


    def search_file_number(self):
        with open(f'datum/setting.txt') as f:
            return int(f.readline())


    def make_folder(self):
        os.mkdir(f'datum/{file_index}')
        os.mkdir(f'datum/{file_index}/images')
        with open(f'datum/{file_index}/number.txt', mode = 'x') as f:
            f.write('0\n')


    def write_setting(self, num):
        with open(f'datum/setting.txt', mode = 'r+') as f:
            f.write(str(num))


    def read_index(self):
        with open(f'datum/{file_index}/number.txt') as f:
            return int(f.readline())


    def write_index(self, text):
        with open(f'datum/{file_index}/number.txt', mode = 'a') as f:
            f.write(text)


    def read_num(self, index, flag):
        tool = pyocr.get_available_tools()[0]

        img = auto.screenshot(region=(173, 490, 480, 225))
        img.save(f'datum/{file_index}/images/image_{index}.png')

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
        index = self.read_index()
        cnt = 0
        flag = False
        while True:
            index += 1
            print('--------------------------')
            auto.click(300,600)
            num = self.read_num(index, flag)

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
                    sleep(0.05)
            sleep(0.05)
            auto.click(300, 600)


            self.write_index(f'{index}, {num},\n')


            print(f'index = {index}, cnt = {cnt}, n = {num}, ans = {ans[1]}')
            sleep(3.7)

#run
create_data = create_data()
create_data.run()