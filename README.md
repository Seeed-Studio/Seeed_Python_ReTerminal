# Python Library for reTerminal

This is a Python library which enables you to use the onboard hardware on the [reTerminal](https://www.seeedstudio.com/ReTerminal-with-CM4-p-4904.html). Currently the **accelerometer, user LEDs, user buttons and buzzer** can be accessed using this Python library.

## Installation

### From PyPI

- To install the latest release from PyPI
```
sudo pip3 install seeed-python-reterminal
```

### From Source

- To install from source, clone this repository
```
git clone https://github.com/Seeed-Studio/Seeed_Python_ReTerminal
```

- Install the library 

```
cd Seeed_Python_ReTerminal
sudo pip3 install .
```

## Usage

### User LEDs Test

```python
import seeed_python_reterminal.core as rt
import time

print("STA ON, USR OFF")
rt.sta_led = True
rt.usr_led = False
time.sleep(1)

print("STA OFF, USR ON")
rt.sta_led = False
rt.usr_led = True
time.sleep(1)

print("STA RED, USR OFF")
rt.sta_led_green = False
rt.sta_led_red = True
rt.usr_led = False
time.sleep(1)

print("STA OFF, USR OFF")
rt.sta_led = False
rt.usr_led = False
```

### Buzzer Test

```python
import seeed_python_reterminal.core as rt
import time

print("BUZZER ON")
rt.buzzer = True
time.sleep(1)

print("BUZZER OFF")
rt.buzzer = False
```

### User Buttons Test

```python
import seeed_python_reterminal.core as rt
import seeed_python_reterminal.button as rt_btn


device = rt.get_button_device()
while True:
    for event in device.read_loop():
        buttonEvent = rt_btn.ButtonEvent(event)
        if buttonEvent.name != None:
            print(f"name={str(buttonEvent.name)} value={buttonEvent.value}")
```

### Accelerometer Test

```python
import seeed_python_reterminal.core as rt
import seeed_python_reterminal.acceleration as rt_accel


device = rt.get_acceleration_device()
while True:
    for event in device.read_loop():
        accelEvent = rt_accel.AccelerationEvent(event)
        if accelEvent.name != None:
            print(f"name={str(accelEvent.name)} value={accelEvent.value}")
```

### Accelerometer and Buttons Test

```python
import asyncio
import seeed_python_reterminal.core as rt
import seeed_python_reterminal.acceleration as rt_accel
import seeed_python_reterminal.button as rt_btn


async def accel_coroutine(device):
    async for event in device.async_read_loop():
        accelEvent = rt_accel.AccelerationEvent(event)
        if accelEvent.name != None:
            print(f"accel name={str(accelEvent.name)} value={accelEvent.value}")


async def btn_coroutine(device):
    async for event in device.async_read_loop():
        buttonEvent = rt_btn.ButtonEvent(event)
        if buttonEvent.name != None:
            print(f"name={str(buttonEvent.name)} value={buttonEvent.value}")


accel_device = rt.get_acceleration_device()
btn_device = rt.get_button_device()

asyncio.ensure_future(accel_coroutine(accel_device))
asyncio.ensure_future(btn_coroutine(btn_device))

loop = asyncio.get_event_loop()
loop.run_forever()
```

## API Reference

- **usr_led**: Turn on/off green USR LED

```python
rt.usr_led = True #Turn on green USR LED
rt.usr_led = False #Turn off green USR LED
```

- **sta_led_red**: Turn on/off red STA LED

```python
rt.sta_led_red = True #Turn on red STA LED
rt.sta_led_red = False #Turn off red STA LED
```

- **sta_led_green**: Turn on/off green STA LED

```python
rt.sta_led_green = True #Turn on green STA LED
rt.sta_led_green = False #Turn off green STA LED
```

**Note:** If red STA LED is on during this time, the green STA LED will turn on over the red STA LED

- **sta_led**: Turn on/off green STA LED

```python
rt.sta_led = True #Turn on green STA LED
rt.sta_led = False #Turn off green STA LED
```

**Note:** If red STA LED is on during this time, the green STA LED will turn on and the red STA LED will turn off

- **buzzer** : Turn on/off buzzer 

```python
rt.buzzer = True #Turn on buzzer
rt.buzzer = False #Turn off buzzer
```
