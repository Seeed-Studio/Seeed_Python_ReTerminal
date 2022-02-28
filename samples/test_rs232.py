#!/usr/bin/env python3

import sys
import serial
import time
import seeed_python_reterminal.core as rt

param1 = sys.argv[1]

# enable the rs232 for test
rt.rs232_or_rs485 = "RS232"

# init the serial
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

if param1 == "send":
    counter=0
    try:
        print("rs232 starts now!\n")
        ser.write("rs232 starts now!\n".encode())
        while 1:
                ser.write(("Write counter:{}\n".format(counter)).encode())
                time.sleep(1)
                counter += 1
    except KeyboardInterrupt:
        exit()
elif param1 == "receive":
    try:
        print("Start receiving data now!\n")
        while 1:
            x=ser.readline()
            if x != b'':
                print(x)
    except KeyboardInterrupt:
        exit()
else:
    print('param input error,try again with send or receive')
