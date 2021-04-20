#!/usr/bin/env python3

import reterminal.core as rt
import time

print("BUZZER ON")
rt.buzzer = 1
time.sleep(1)

print("BUZZER OFF")
rt.buzzer = 0
