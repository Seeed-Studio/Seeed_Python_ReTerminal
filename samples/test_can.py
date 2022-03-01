#!/usr/bin/env python3

import os 
import sys
import time

param1 = sys.argv[1]

if param1 == "send":
    counter=0
    print("can send starts now!\n")
    try:
        while counter < 10:
            os.system('cansend can0 111#0' + str(counter))
            time.sleep(1)
            counter += 1
    except KeyboardInterrupt:
        exit()
elif param1 == "receive":
    print("can start receiving data now!\n")
    try:
        os.system('candump can0')
    except KeyboardInterrupt:
        exit()
else:
    print('param input error,try again with send or receive')
