#!/usr/bin/env python3
from multiprocessing import Process

import os

p = None

def f():
    #while True:
    print('PID:  ' + str(os.getpid()))


if __name__ == '__main__':
    p = Process(target=f)
    p.start()
    flag = True
    while flag:
        print(p)
        msg = input()
        if "quit" in msg:
            p.terminate()
            flag = False
