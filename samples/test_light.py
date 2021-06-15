#!/usr/bin/env python3

import time
import seeed_python_reterminal.core as rt

while True:
    print(rt.illuminance)
    time.sleep(0.2)
