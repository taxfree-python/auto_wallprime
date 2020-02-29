#import
from mode import mode_choice
from get_number import get_number
from read_num import read_num
from auto_click import auto_click_insane
from time import sleep
import pyautogui as auto


#パラメータ
mode = 'insane'
auto.click(70,150)

#solve
while True:
    m = 0
    error_counter = 0
    while error_counter < 5:
        img = get_number()
        n = read_num()
        if n == 'error':
            error_counter += 1
            print('error')
            continue
        else:
            error_counter = 0
            break
    else:
        print('please type number cannot read')
        n = int(input())
        error_counter = 0

    print(n)
    prime_f = mode_choice(mode)
    cal = []
    error_counter = 0
    while n >= 2:
        for i in prime_f:
            if n % i == 0:
                cal.append(i)
                n /= i
                error_counter = 0
            elif error_counter > 16:
                break
            else:
                error_counter += 1
        else:
            continue
        break
    if error_counter > 16:
        print('please type number read error')
        n = int(input())
        m += n
        cal = []
        error_counter = 0
        while n >= 2:
            for i in prime_f:
                if n % i == 0:
                    cal.append(i)
                    n /= i
                    error_counter = 0
                elif error_counter > 16:
                    break
                else:
                    error_counter += 1
            else:
                n = m
                break
    cal.sort()
    for s in range(len(cal)):
        auto_click_insane(cal[s])
        sleep(0.05)
    print(cal)
    auto.click(300,600)
    sleep(3.5)