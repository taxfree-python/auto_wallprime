#import
from mode import mode_choice
from get_number import get_number
from read_num import read_num
from auto_click import auto_click_insane, stop_click, resume_click, close_tab
from show_prime import show_prime
from time import sleep
import pyautogui as auto

#パラメータ
mode = 'insane'
auto.click(70,150)

#solve
while True:
    breaker = True
    print('--------------------------')
    error_counter = 0
    while error_counter < 3:
        get_number()
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
        stop_click()
        show_prime()
        n = int(input())
        close_tab()
        sleep(0.05)
        resume_click()
        error_counter = 0

    print(n)
    prime_f = mode_choice(mode)
    cal = []
    error_counter = 0
    if n == 1:
        auto.click(300,600)
    while n != 1:
        for i in prime_f:
            if n % i == 0:
                cal.append(i)
                n /= i
                n = int(n)
                error_counter = 0
                print('n =',n,'  ',i)
            elif error_counter > 16:
                break
            else:
                error_counter += 1
        else:
            continue
        break
    print(error_counter)
    if error_counter > 16:
        print(n)
        print('please type number read error')
        stop_click()
        show_prime()
        n = int(input())
        close_tab()
        sleep(0.05)
        cal = []
        resume_click()
        sleep(0.05)
        error_counter = 0
        while n != 1:
            for i in prime_f:
                if n % i == 0:
                    cal.append(i)
                    n /= i
                    n = int(n)
                    error_counter = 0
                elif error_counter > 16:
                    breaker = False
                    break
                else:
                    error_counter += 1
            else:
                continue
            break
    for s in range(len(cal)):
        sleep(0.05)
        auto_click_insane(cal[s])
    print(cal)
    auto.click(300,600)
    if breaker:
        sleep(3.5)