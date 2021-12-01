import cv2
import numpy as np
from read_num import read_num_img, read_num_path
from PIL import Image
from multiprocessing import Pool
import pyocr
import re
import time


class Optimizer:

    def review(self, path):
        '''
        for i in range(1):
            original = cv2.imread(f'datasets/dataset_1/image_{i}.png')
            img = self.comb(original)
            original = Image.fromarray(original)

            imgs = [original, img]
            ans = p.map(self.read_num_img, imgs)

            #cv2.imwrite(f'datum/diff/diff_{i}.png', np.array(img))

            print(ans)
            if ans[1][0] == corrects[i - 1] and ans[1][1] == corrects[i - 1]:
                correct += 1
            elif ans[1][0] == corrects[i - 1] or ans[1][1] == corrects[i - 1]:
                print(f'{i}, {corrects[i - 1]}, {ans[0]}→{ans[1]}')
                probably += 1
            elif corrects[i - 1] != 0:
                print(f'{i}, {corrects[i - 1]}, {ans[0]}→{ans[1]}')
                wrong += 1

            if i % 10 == 0:
                print('working')
        return f'reslt = {correct}, {probably}, {wrong}'
        '''

        #model_1
        start = time.time()
        with open(f'{path}/correct.txt') as f:
            corrects = [int(s) for s in f.readlines()]

        length = len(corrects)
        score = [0, 0, 0, 0] #both, ans[0], ans[1], neither

        index = [i for i in range(length)]
        p = Pool(6)
        ans_eng = p.map(self.read_num_img_eng, index)
        ans_snum = p.map(self.read_num_img_snum, index)

        cnt = 0
        for eng, snum, correct in zip(ans_eng, ans_snum, corrects):
            if eng == snum == correct:
                score[0] += 1
            elif eng == correct:
                score[1] += 1
            elif snum == correct:
                score[2] += 1
            else:
                print(cnt, eng, snum, correct)
                score[3] += 1
            cnt += 1

        fin = time.time()
        print(f'used time is {fin - start}')
        return score


        '''
        #model_2
        start = time.time()
        with open(f'{path}/correct.txt') as f:
            corrects = [int(s) for s in f.readlines()]

        length = len(corrects)
        score = [0, 0, 0, 0] #both, ans[0], ans[1], neither

        p = Pool(6)
        for i in range(length):
            img = self.comb(cv2.imread(f'{path}/image_{i}.png'))
            datum = [(img, 'eng'), (img, 'snum')]

            ans = p.map(self.read_num_img, datum)

            if ans[0] == corrects[i] == ans[0] == ans[1]:
                score[0] += 1
            elif ans[0] == corrects[i]:
                score[1] += 1
            elif ans[1] == corrects[i]:
                score[2] += 1
            else:
                score[3] += 1

        fin = time.time()
        print(f'used time is {fin - start}')
        return score
        '''


    def read_num_img_eng(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.comb(cv2.imread(f'{path}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img_snum(self, index):
        tool = pyocr.get_available_tools()[0]

        img = self.comb(cv2.imread(f'{path}/image_{index}.png'))
        num = int(re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8))) or 0)

        return num


    def read_num_img(self, datum):
        tool = pyocr.get_available_tools()[0]

        num_eng = re.sub(r'\D', '', tool.image_to_string(datum[0], lang = datum[1], builder = pyocr.builders.DigitBuilder(tesseract_layout = 8)))

        ans = int(num_eng or 0)
        return ans


    def inv(self, diff): #二値化，白黒反転
        ret, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY_INV)

        return diff


    def findcon(self, diff): #輪郭抽出
        x_size, y_size = diff.shape[0], diff.shape[1]
        edge = cv2.Canny(diff, 255, 260, True)

        cv2.imwrite('edge.png', edge)
        contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        app = []
        for i in range(len(contours)):
            length = cv2.arcLength(contours[i], True)
            app.append((contours[i], length))

        app.sort(key = lambda x: x[1], reverse = True)

        emp = np.zeros((x_size, y_size))
        diff = cv2.drawContours(emp, contours, -1, (255, 0, 0), 2) #2

        diff = Image.fromarray(diff)
        return diff


    def rot(self, diff): #回転
        x_size = diff.shape[0]
        y_size = diff.shape[1]

        trans = cv2.getRotationMatrix2D((int(x_size / 2), int(y_size / 2)), -2, 0.9)
        diff = cv2.warpAffine(diff, trans, (y_size, x_size), borderValue=(255, 255, 255))

        diff = Image.fromarray(diff)
        return diff


    def trimming(self, diff): #トリミング
        diff[168:, :45] = [[255, 255, 255]]
        diff[0:, :20] = [[255, 255, 255]]

        diff = Image.fromarray(diff)
        return diff


    def comb(self, diff):
        diff = np.array(self.inv(diff))
        diff = np.array(self.trimming(diff))
        diff = self.rot(diff)
        return diff
        #return Image.fromarray(diff)




path = 'datasets/dataset_2'
if __name__ == '__main__':
    opt = Optimizer()
    print(opt.review(path))