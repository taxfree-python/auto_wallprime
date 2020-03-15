#import
import pyautogui as auto

def auto_click_insane(cal):
    if cal == 2:
        auto.click(45,490)
    elif cal == 3:
        auto.click(100,490)
    elif cal == 5:
        auto.click(160,490)
    elif cal == 7:
        auto.click(210,490)
    elif cal == 11:
        auto.click(45,540)
    elif cal == 13:
        auto.click(100,540)
    elif cal == 17:
        auto.click(160,540)
    elif cal == 19:
        auto.click(210,540)
    elif cal == 23:
        auto.click(45,590)
    elif cal == 29:
        auto.click(100,590)
    elif cal == 31:
        auto.click(160,590)
    elif cal == 37:
        auto.click(210,590)
    elif cal == 41:
        auto.click(45,640)
    elif cal == 43:
        auto.click(100,640)
    elif cal == 47:
        auto.click(160,640)
    elif cal == 53:
        auto.click(210,640)

def stop_click():
    auto.click(330,85)

def resume_click():
    auto.click(180,430)

def close_tab():
    auto.click(18,37)