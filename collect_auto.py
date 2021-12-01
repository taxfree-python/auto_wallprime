#import
import os
from random import randint, choice
from time import sleep
import re
from PIL import Image
import pyocr
import pyautogui as auto
from multiprocessing import Pool
import cv2


class collect_auto:

    def __init__(self):
        self.run()

    def read_num_multi(self, param):
        tool = pyocr.get_available_tools()[0]
        image = cv2.imread(f'datum/images/image_{param[1]}.png')

        ret, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
        x_size = image.shape[0]
        y_size = image.shape[1]

        image[168:, :45] = [[255, 255, 255]]
        image[0:, :20] = [[255, 255, 255]]

        trans = cv2.getRotationMatrix2D((int(x_size / 2), int(y_size / 2)), -3, 0.9)
        img = cv2.warpAffine(image, trans, (y_size, x_size), borderValue=(255, 255, 255))

        img = Image.fromarray(img)
        num = re.sub(r'\D', '', tool.image_to_string(img, lang = f'{param[0]}', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8)))

        return (int(num or 0))


    def auto_click(self, pos):
        x = [50, 105, 160, 215]
        y = [495, 545, 600, 650]
        r = randint(-8, 8)
        auto.click(x[pos % 4] + r, y[pos // 4] + r)


    def check(self, nums):
        if nums[0] == 0:
            return nums[1]
        elif nums[1] == 0:
            return nums[0]
        elif nums[0] != nums[1]:
            return choice(nums)
        else:
            return nums[0]


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
        ind = 1000
        p = Pool(6)
        for _ in range(10**9):
            ind += 1

            auto.click(300,600)
            img = auto.screenshot(region = (175, 490, 480, 225))
            img.save(f'datum/images/image_{ind}.png')

            langs = [('eng', ind), ('snum', ind)]
            numbers = p.map(self.read_num_multi, langs)
            num = self.check(numbers)

            print(numbers)
            print(num)
            ans = self.pfactorization(num)
            status = ans[0]
            cal = ans[1]

            if status == 0:
                print(f'n = {num}, failed pfactorization')
                continue

            for i in range(16):
                for _ in range(cal[i]):
                    self.auto_click(i)
                    sleep(0.05)
            auto.click(300, 600)

            sleep(3.1)



#run
if __name__ == "__main__":
    collect_auto()