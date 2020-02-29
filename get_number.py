#import
import pyautogui as auto

def get_number():
    img = auto.screenshot(region=(180,370,420,400))
    img.save('image/prime.png')