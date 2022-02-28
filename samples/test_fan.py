#!/usr/bin/env python3

import seeed_python_reterminal.core as rt
import time

print("FAN ON")
rt.fan = True
time.sleep(1)

print("FAN OFF")
rt.fan = False
