import cv2
import numpy as np
from read_num import read_num_img, read_num_path
from PIL import Image
from multiprocessing import Pool
import pyocr
import re
import time
import csv

class Reviewer:
    def review(self, method, param, num):
        start = time.time()

        with open(f'datasets/dataset_{num}/correct.txt') as f:
            corrects = [int(s) for s in f.readlines()]

        length = len(corrects)
        score = [0, 0, 0, 0] #both, eng, snum, other
        index = [(num, i) for i in range(length)]

        if method == 0:
            p = Pool(2)
            ans_eng = p.map(self.read_num_img_eng_0, index)
            ans_snum = p.map(self.read_num_img_snum_0, index)

        if method == 1:
            p = Pool(8)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_img_eng_1, index)
            ans_snum = p.map(self.read_num_img_snum_1, index)
        elif method == 2:
            p = Pool(2)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_img_eng_2, index)
            ans_snum = p.map(self.read_num_img_snum_2, index)
        elif method == 3:
            p = Pool(7)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_img_eng_3, index)
            ans_snum = p.map(self.read_num_img_snum_3, index)
        elif method == 4:
            p = Pool(2)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_img_eng_4, index)
            ans_snum = p.map(self.read_num_img_snum_4, index)
        elif method == 5:
            p = Pool(2)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_img_eng_5, index)
            ans_snum = p.map(self.read_num_img_snum_5, index)
        elif method == 6:
            p = Pool(2)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_img_eng_6, index)
            ans_snum = p.map(self.read_num_img_snum_6, index)


        cnt = 0
        for eng, snum, correct in zip(ans_eng, ans_snum, corrects):
            if eng == snum == correct:
                score[0] += 1
            elif eng == correct:
                score[1] += 1
            elif snum == correct:
                score[2] += 1
            else:
                score[3] += 1
            cnt += 1

        fin = time.time()
        t = round(fin - start, 2)

        with open(f'method_{method}.csv', 'a') as f:
            write = csv.writer(f)
            write.writerow([param, num] + score + [score[0] + score[1] + score[2], round((score[0] + score[1] + score[2]) / length * 100, 2)])

        return t

    def read_num_img_eng_0(self, index):
        tool = pyocr.get_available_tools()[0]

        img = Image.fromarray(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_0(self, index):
        tool = pyocr.get_available_tools()[0]

        img = Image.fromarray(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_1(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_1(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_2(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_2(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png', 0), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_3(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_3(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_4(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_4(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_5(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_5(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_6(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_6(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_1(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_1(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_2(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_2(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png', 0), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_3(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_3(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_4(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_4(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_5(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_5(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_6(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_6(cv2.imread(f'datasets/dataset_{index[0]}/image_{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def method_1(self, diff, param): #回転
        x_size = diff.shape[0]
        y_size = diff.shape[1]

        trans = cv2.getRotationMatrix2D((int(x_size / 2), int(y_size / 2)), param, 0.7)
        diff = cv2.warpAffine(diff, trans, (y_size, x_size), borderValue = (255, 255, 255))

        diff = Image.fromarray(diff)
        return diff


    def method_2(self, diff, param): #二値化，白黒反転
        ret, diff = cv2.threshold(diff, param, 255, cv2.THRESH_BINARY_INV)

        diff = Image.fromarray(diff)
        return diff


    def method_3(self, diff, param):
        diff = cv2.GaussianBlur(diff, (param, param,), 3)

        diff = Image.fromarray(diff)
        return diff


    def method_4(self, diff, param): #輪郭抽出
        x_size, y_size = diff.shape[0], diff.shape[1]
        edge = cv2.Canny(diff, 400, 410, True)

        contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        emp = np.ones((x_size, y_size))

        cnt = []
        for i in range(len(contours)):
            flag = True
            for j in range(len(contours[i])):
                if contours[i][j][0][1] > 200:
                    flag = False
            if flag:
                cnt.append(contours[i])

        diff = cv2.drawContours(emp, cnt, -1, 0, param)

        diff = Image.fromarray(diff)
        return diff


    def method_5(self, diff, param): #トリミング
        diff[165:, :50] = [[0, 0, 0]] #black
        diff[0:, :20] = [[0, 0, 0]] #black

        diff = Image.fromarray(diff)
        return diff


    def method_6(self, diff, param):
        diff = np.array(self.method_5(diff, [165, 45, 0, 30]))
        diff = self.method_2(diff, 170)

        return diff





method = 5

if __name__ == '__main__':
    rev = Reviewer()
    for i in range(9, 10): #param
        for j in range(1, 6): #dataset
            print(rev.review(method, i, j))

        with open(f'method_{method}.csv', 'a') as f:
            write = csv.writer(f)
            write.writerow('')

        #time.sleep(60)