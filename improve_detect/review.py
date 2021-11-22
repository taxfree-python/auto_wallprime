import cv2
import numpy as np
from read_num import read_num_img, read_num_path
from PIL import Image
from multiprocessing import Pool
import pyocr
import re


class Optimizer:

    def review(self):
        methods = ['findcon']
        with open('datum/number.txt') as f:
            length = int(f.readline())

        with open('datum/correct_num.txt') as f:
            corrects = [int(s[:-1]) for s in f.readlines()]

        correct = 0
        probably = 0
        wrong = 0

        p = Pool(6)

        for i in range(12, 13):
            original = cv2.imread(f'datum/images/image_{i}.png')
            img = self.comb(original)
            original = Image.fromarray(original)

            #img.show()
            imgs = [original, img]
            ans = p.map(self.read_num_img, imgs)


            if ans[1][0] == corrects[i - 1] and ans[1][1] == corrects[i - 1]:
                correct += 1
            elif ans[1][0] == corrects[i - 1] or ans[1][1] == corrects[i - 1]:
                print(f'{corrects[i - 1]}, {ans[0]}→{ans[1]}')
                probably += 1
            else:
                wrong += 1

            if i % 10 == 0:
                #print(f'{corrects[i - 1]}, {ans[0]}→{ans[1]}')
                print('working')
        return f'reslt = {correct}, {probably}, {wrong}'


    def read_num_img(self, img):
        tool = pyocr.get_available_tools()[0]

        num_eng = re.sub(r'\D', '', tool.image_to_string(img, lang = 'eng', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8)))
        num_snum  = re.sub(r'\D', '', tool.image_to_string(img, lang = 'snum', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8)))

        ans = (int(num_eng or 0), int(num_snum or 0))
        return ans


    def opt(self, diff):
        ret, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY_INV)

        return diff


    def findcon(self, diff):
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


    def rot(self, diff):
        x_size = diff.shape[0]
        y_size = diff.shape[1]

        trans = cv2.getRotationMatrix2D((int(x_size / 2), int(y_size / 2)), -5, 1.0)
        image = cv2.warpAffine(diff, trans, (x_size, y_size))

        diff = Image.fromarray(diff)
        return diff


    def trimming(self, diff):
        diff[168:, :45] = [[255, 255, 255]]
        diff[0:, :20] = [[255, 255, 255]]

        diff = Image.fromarray(diff)
        return diff


    def comb(self, diff):
        diff = np.array(self.opt(diff))
        diff = np.array(self.trimming(diff))
        diff = self.rot(diff)
        #diff = self.findcon(diff)
        return diff

if __name__ == '__main__':
    opt = Optimizer()
    print(opt.review())