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

