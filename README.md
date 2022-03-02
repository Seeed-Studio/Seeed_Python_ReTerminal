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

**The Following Test Should Work With Reterminal Bridge**

### fan Test

```python
import seeed_python_reterminal.core as rt
import time

print("FAN ON")
rt.fan = True
time.sleep(1)

print("FAN OFF")
rt.fan = False
```

### RS232 Test

```python
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
```
**Note:**:When we use the test script of RS232/RS485/CAN.We need to pass a parameter to them.

Take the RS232 for example:
```
python3 test_rs232.py send # test the send(TX) function of RS232
python3 test_rs232.py receive # test the receive(RX) function of RS232
```

### RS485 Test

```python
import sys
import serial
import time
import seeed_python_reterminal.core as rt

param1 = sys.argv[1]

# enable the rs485 for test
rt.rs232_or_rs485 = "RS485"

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
    # enable the rs485 for tx
    rt.rs485_tx_rx_stat = "TX"
    try:
        print("rs485 starts now!\n")
        ser.write("rs485 starts now!\n".encode())
        while 1:
                ser.write(("Write counter:{}\n".format(counter)).encode())
                time.sleep(1)
                counter += 1
    except KeyboardInterrupt:
        exit()
elif param1 == "receive":
    # enable the rs485 for rx
    rt.rs485_tx_rx_stat = "RX"
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
```

### CAN Test

```python
# NOTICE: please make sure you have pip3 install python-can
#         before you use this test script
# import the library
import can
import sys
import time

param1 = sys.argv[1]

# create a bus instance
# many other interfaces are supported as well (see documentation)
bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)

if param1 == "send":
    # send a message
    counter=0
    print("can send starts now!\n")
    try:
        while True:
            message = can.Message(arbitration_id=123, is_extended_id=True,
                      data=[0x11, 0x22, counter])
            bus.send(message, timeout=0.2)
            time.sleep(1)
            counter += 1
    except KeyboardInterrupt:
        exit()

elif param1 == "receive":
    # iterate over received messages
    try:
        for msg in bus:
            print(f"{msg.arbitration_id:X}: {msg.data}")
    except KeyboardInterrupt:
        exit()
else:
    print('param input error,try again with send or receive')
```
**Note:** Please make sure your CAN interface is working before run this script.
If not. You will get the error log with "Network is down". And you can 
enable the can with "sudo ip link set can0 up type can bitrate 500000".

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

- **get_button_device()**: Obtain information about the buttons including all the events supported by them

```python
device = rt.get_button_device()
```

- **ButtonEvent()**: Calls the ButtonEvent() and returns the EVENT

```python
buttonEvent = rt_btn.ButtonEvent(event)
```

- **get_acceleration_device()**: Obtain information about the accelerometer including all the events supported by it 

```python
device = rt.get_acceleration_device()
```

- **AccelerationEvent()**: Calls the AccelerationEvent() and returns the EVENT

```python
accelEvent = rt_accel.AccelerationEvent(event)
```

- **fan**: Turn on/off fan

```python
rt.fan = True # Turn on fan
rt.fan = False # Turn off fan
```

- **rs232_or_rs485**: Open the RS232 or RS485

```python
rt.rs232_or_rs485 = "RS232" # open the RS232
rt.rs232_or_rs485 = "RS485" # open the RS485
```

- **rs485_tx_rx_stat**: Switch the function between send(TX) and receive(Rx) of RS485

```python
rt.rs485_tx_rx_stat = "TX" # enable the send(TX) of RS485
rt.rs485_tx_rx_stat = "RX" # enable the receive(RX) of RS485
```
