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
    def review(self, path, method):
        start = time.time()

        with open(f'{sample_name}/correct.txt') as f:
            corrects = [int(s) for s in f.readlines()]

        length = len(corrects)
        score = [0, 0, 0, 0] #both, ans[0], ans[1], neither

        index = [i for i in range(length)]

        if method == 1:
            p = Pool(6)
            ans_eng = p.map(self.read_num_img_eng_1, index)
            ans_snum = p.map(self.read_num_img_snum_1, index)
        elif method == 2:
            p = Pool(6)
            ans_eng = p.map(self.read_num_img_eng_2, index)
            ans_snum = p.map(self.read_num_img_snum_2, index)
        elif method == 3:
            p = Pool(6)
            ans_eng = p.map(self.read_num_img_eng_3, index)
            ans_snum = p.map(self.read_num_img_snum_3, index)
        elif method == 4:
            p = Pool(6)
            ans_eng = p.map(self.read_num_img_eng_4, index)
            ans_snum = p.map(self.read_num_img_snum_4, index)
        elif method == 5:
            p = Pool(6)
            ans_eng = p.map(self.read_num_img_eng_5, index)
            ans_snum = p.map(self.read_num_img_snum_5, index)
        elif method == 6:
            p = Pool(6)
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
        print(t)

        with open('method_1.csv', 'a') as f:
            write = csv.writer(f)



            write.writerow([param, number] + score)




        return score


    def read_num_img_eng_1(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_1(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_2(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_2(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_3(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_3(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_4(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_4(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_5(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_5(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_eng_6(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_6(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_1(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_1(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_2(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_2(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_3(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_3(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_4(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_4(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_5(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_5(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum_6(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_6(cv2.imread(f'{sample_name}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def method_1(self, diff): #回転
        x_size = diff.shape[0]
        y_size = diff.shape[1]

        trans = cv2.getRotationMatrix2D((int(x_size / 2), int(y_size / 2)), param, 0.9)
        diff = cv2.warpAffine(diff, trans, (y_size, x_size), borderValue = (255, 255, 255))

        #cv2.imwrite('rot.png', diff)
        diff = Image.fromarray(diff)
        return diff


    def method_2(self, diff): #二値化，白黒反転
        ret, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY_INV)

        diff = Image.fromarray(diff)
        return diff


    def method_3(self, diff):
        diff = cv2.GaussianBlur(diff, (7, 7,), 3)

        diff = Image.fromarray(diff)
        return diff


    def method_4(self, diff): #輪郭抽出
        x_size, y_size = diff.shape[0], diff.shape[1]
        edge = cv2.Canny(diff, 255, 260, True)

        #cv2.imwrite('edge.png', edge)
        contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        emp = np.zeros((x_size, y_size))
        diff = cv2.drawContours(emp, contours, -1, (255, 0, 0), 2)

        diff = Image.fromarray(diff)
        return diff


    def method_5(self, diff): #トリミング
        diff[168:, :45] = [[255, 255, 255]]
        diff[0:, :20] = [[255, 255, 255]]

        diff = Image.fromarray(diff)
        return diff


    def method_6(self, diff):
        #diff = np.array(self.method_3(diff))
        diff = np.array(self.method_2(diff))
        diff = np.array(self.method_5(diff))
        diff = np.array(self.method_1(diff))
        diff = self.method_4(diff)
        return diff
        #return Image.fromarray(diff)




number = 5
sample_name = 'datasets/dataset_' + str(number)
method = 1
param = 4


if __name__ == '__main__':
    rev = Reviewer()
    print(rev.review(sample_name, method))