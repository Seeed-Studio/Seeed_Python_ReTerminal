from enum import Enum
import evdev


class ButtonName(Enum):
    F1 = 1
    F2 = 2
    F3 = 3
    O = 4


class ButtonEvent:

    def __init__(self, event):
        if event.type == evdev.ecodes.EV_KEY:
            if event.code == 30:
                self.name = ButtonName.F1
                self.value = event.value
            elif event.code == 31:
                self.name = ButtonName.F2
                self.value = event.value
            elif event.code == 32:
                self.name = ButtonName.F3
                self.value = event.value
            elif event.code == 33:
                self.name = ButtonName.O
                self.value = event.value
            else:
                self.name = None
                self.value = None
        else:
            self.name = None
            self.value = None
