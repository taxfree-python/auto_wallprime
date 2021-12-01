from multiprocessing import Pool
import multiprocessing as multi
import time
from random import choice
from read_num import read_num_eng, read_num_snum, read_num_lang


def check(ans):
    if ans[0] == 0 and ans[1] == 0:
        return (0, ans)
    elif ans[0] == 0: #一桁の数字で出やすい
        return (2, ans)
    elif ans[0] == 1 and ans[1] != 1:
        return (2, ans)
    elif ans[0] != ans[1] and ans[0] // 10 == ans[1]:
        return (2, ans)
    elif ans[0] != ans[1]:
        c = choice(list(ans))
        ans = (c, c)
        return (1, ans)
    else:
        return (1, ans)


if __name__ == "__main__":
    n = 10
    '''
    start = time.time()
    nums = []
    for _ in range(n):
        nums.append([read_num_lang('eng'), read_num_lang('snum')])
    print(f'used time is {time.time() - start}')
    '''
    start = time.time()
    langs = ['eng', 'snum']
    nums_multi = []
    process = Pool(multi.cpu_count() - 1)
    for _ in range(n):
        nums_multi.append(check((((process.map(read_num_lang, langs))))))
    process.close()
    print(f'used time is {time.time() - start}')
    print(nums_multi)

