import cv2
import numpy as np
from PIL import Image
from multiprocessing import Pool
import pyocr
import re
#import time
import csv


class Evaluate_method:
    def evaluate_method(self, method, param, num): #method, param, dataset_number
        #start = time.time()

        with open(f'data/dataset_{num}/correct.txt') as f:
            corrects = [int(s) for s in f.readlines()]

        with open(f'data/dataset_{num}/score.txt') as f:
            scores = [int(s) for s in f.readlines()]

        length = len(corrects)

        if method == 0:
            p = Pool(6)
            index = [(num, i) for i in range(length)]
            ans_eng = p.map(self.read_num_eng_0, index)
            ans_snum = p.map(self.read_num_snum_0, index)

        if method == 1:
            p = Pool(8)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_eng_1, index)
            ans_snum = p.map(self.read_num_snum_1, index)
        elif method == 2:
            p = Pool(3)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_eng_2, index)
            ans_snum = p.map(self.read_num_snum_2, index)
        elif method == 3:
            p = Pool(3)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_eng_3, index)
            ans_snum = p.map(self.read_num_snum_3, index)
        elif method == 4:
            p = Pool(8)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_eng_4, index)
            ans_snum = p.map(self.read_num_snum_4, index)
        elif method == 5:
            p = Pool(3)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_eng_5, index)
            ans_snum = p.map(self.read_num_snum_5, index)
        elif method == 6:
            p = Pool(8)
            index = [(num, i, param) for i in range(length)]
            ans_eng = p.map(self.read_num_eng_6, index)
            ans_snum = p.map(self.read_num_snum_6, index)


        res = [0, 0, 0, 0] #both, eng, snum, wrong
        for eng, snum, correct in zip(ans_eng, ans_snum, corrects):
            if eng == snum == correct:
                res[0] += 1
            elif eng == correct:
                res[1] += 1
            elif snum == correct:
                res[2] += 1
            else:
                #print(cnt, ans_eng[cnt], ans_snum[cnt], corrects[cnt])
                res[3] += 1

        #fin = time.time()
        #t = round(fin - start, 2)
        if res[1] + res[2] == 0:
            weighted_eng = 0.500
            weighted_snum = 0.500
        else:
            weighted_eng = res[1] / (res[1] + res[2])
            weighted_snum = res[2] / (res[1] + res[2])

        score = 0
        for i in range(length):
            eng = ans_eng[i]
            snum = ans_snum[i]
            correct = corrects[i]

            if eng == snum == correct:
                score += scores[i]
            elif eng == correct:
                score += weighted_eng * scores[i]
            elif snum == correct:
                score += weighted_snum * scores[i]

        with open(f'evaluation/method_{method}.csv', 'a') as f:
            write = csv.writer(f)
            write.writerow([param, num] + res + [round((res[0] + res[1] + res[2]) / length * 100, 2), int(score), round(weighted_eng, 2), round(weighted_snum, 2)])
            #write.writerow([param, num] + score + [score[0] + score[1] + score[2], round((score[0] + score[1] + score[2]) / length * 100, 2)])

        return int(score)

    def read_num_eng_0(self, index):
        tool = pyocr.get_available_tools()[0]

        img = Image.fromarray(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_snum_0(self, index):
        tool = pyocr.get_available_tools()[0]

        img = Image.fromarray(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_eng_1(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_1(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_eng_2(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_2(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_eng_3(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_3(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_eng_4(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_4(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_eng_5(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_5(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_eng_6(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_6(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_snum_1(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_1(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_snum_2(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_2(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_snum_3(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_3(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_snum_4(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_4(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_snum_5(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_5(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_snum_6(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.method_6(cv2.imread(f'data/dataset_{index[0]}/{index[1]}.png'), index[2])
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def method_1(self, diff, param): #回転
        x_size = diff.shape[0]
        y_size = diff.shape[1]

        trans = cv2.getRotationMatrix2D((int(x_size / 2), int(y_size / 2)), param[0], param[1])
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
        x_size = diff.shape[0]
        y_size = diff.shape[1]
        edge = cv2.Canny(diff, 570, 570, True)

        contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        emp = np.ones((x_size, y_size)) * 255
        diff = cv2.drawContours(emp, contours, -1, 0, 1)

        diff = Image.fromarray(diff)
        return diff


    def method_5(self, diff, param): #トリミング
        diff[param[0]:, :param[1]] = [[0, 0, 0]] #black
        diff[param[2]:, :param[3]] = [[0, 0, 0]] #black

        diff = Image.fromarray(diff)
        return diff


    def method_6(self, diff, param):
        diff = np.array(self.method_1(diff, param[0]))
        diff = np.array(self.method_2(diff, param[1]))
        diff = self.method_2(diff, 180)

        return diff



params = [[(i, 1.0) for i in range(-5, 6)], #method_1
          [i for i in range(225, 241, 5)], #method_2
          [i for i in range(1, 22, 2)], #method_3
          [i for i in range(500, 800, 10)], #method_4
          [(160, 45, 0, 10), (160, 45, 0, 20), (160, 45, 0, 30), (160, 45, 0, 40),
            (165, 45, 0, 10), (165, 45, 0, 20), (165, 45, 0, 30), (165, 45, 0, 40),
            (170, 45, 0, 10), (170, 45, 0, 20), (170, 45, 0, 30), (170, 45, 0, 40),
            (175, 45, 0, 10), (175, 45, 0, 20), (175, 45, 0, 30), (175, 45, 0, 40)],  #method_5
          [[(-2, 0.9), 180]]] #method_6



if __name__ == '__main__':
    Eva = Evaluate_method()
    for i in range(6, 7): #method
        if i == 0:
            print('evaluate method_0')
            score = 0
            for number in range(1, 4):
                score += Eva.evaluate_method(0, 0, number)

            with open('evaluation_method/csv/method_0.csv', 'a') as f:
                write = csv.writer(f)
                write.writerow([score])
        if i == 1 : #method_1
            print('evaluate method_1')
            for param in params[0]: #params
                score = 0
                for number in range(1, 4): #dataset_number
                    score += Eva.evaluate_method(1, param, number)

                with open('evaluation_method/csv/method_1.csv', 'a') as f:
                    write = csv.writer(f)
                    write.writerow([score])

        if i == 2: #method_2
            print('evaluate method_2')
            for param in params[1]:
                score = 0
                for number in range(1, 4):
                    score += Eva.evaluate_method(2, param, number)

                with open('evaluation_method/csv/method_2.csv', 'a') as f:
                    write = csv.writer(f)
                    write.writerow([score])

        if i == 3: #method_3
            print('evaluate method_3')
            for param in params[2]:
                score = 0
                for number in range(1, 4):
                    score += Eva.evaluate_method(3, param, number)

                with open('evaluation_method/csv/method_3.csv', 'a') as f:
                    write = csv.writer(f)
                    write.writerow([score])

        if i == 4: #method_4
            print('evaluate method_4')
            for param in params[3]:
                score = 0
                for number in range(1, 4):
                    score += Eva.evaluate_method(4, param, number)

                with open('evaluation_method/csv/method_4.csv', 'a') as f:
                    write = csv.writer(f)
                    write.writerow([score])

        if i == 5: #method_5
            print('evaluate method_5')
            for param in params[4]:
                score = 0
                for number in range(1, 4):
                    score += Eva.evaluate_method(5, param, number)

                with open('evaluation_method/csv/method_5.csv', 'a') as f:
                    write = csv.writer(f)
                    write.writerow([score])

        if i == 6: #method_6
            print('evaluate method_6')
            for param in params[5]:
                score = 0
                for number in range(1, 4):
                    score += Eva.evaluate_method(6, param, number)

                with open('evaluation_method/csv/method_6.csv', 'a') as f:
                    write = csv.writer(f)
                    write.writerow([score])