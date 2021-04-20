#!/usr/bin/env python3

import reterminal.core as rt
import time

print("STA ON, USR OFF")
rt.sta_led = 1
rt.usr_led = 0
time.sleep(1)

print("STA OFF, USR ON")
rt.sta_led = 0
rt.usr_led = 1
time.sleep(1)

print("STA OFF, USR OFF")
rt.sta_led = 0
rt.usr_led = 0
