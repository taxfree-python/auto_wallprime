import os
from random import randint, choice
from time import sleep, time
import re
from PIL import Image,ImageOps
from multiprocessing import Pool
import multiprocessing as multi
import pyocr
import pyautogui as auto
from collections import defaultdict

def read_num(self, lang):
        tool = pyocr.get_available_tools()[0]

        img = auto.screenshot(region=(175, 490, 480, 225))

        img = img.point(lambda x: x * 1.2).convert('L').point(lambda x: 0 if x < 230 else x)
        img = ImageOps.invert(img)

        num = re.sub(r'\D', '', tool.image_to_string(img, lang = f'{lang}', builder = pyocr.builders.DigitBuilder(tesseract_layout = 8)))

        return num