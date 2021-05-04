from enum import Enum
import evdev


class AccelerationName(Enum):
    X = 0
    Y = 1
    Z = 2


class AccelerationEvent:

    def __init__(self, event):
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == 0:
                self.name = AccelerationName.X
                self.value = event.value
            elif event.code == 1:
                self.name = AccelerationName.Y
                self.value = event.value
            elif event.code == 2:
                self.name = AccelerationName.Z
                self.value = event.value
            else:
                self.name = None
                self.value = None
        else:
            self.name = None
            self.value = None
