import sys
import glob
import evdev
import time
from pathlib import Path
import gpiod
from .board.reterminal_bridge import reterminal_bridge as board_class

# Match the content of the /sys/firmware/devicetree/base/hardware file
board_name = Path("/sys/firmware/devicetree/base/hardware").read_text().strip()
# Check the file names under the board folder, if a file name is contained in board_name, import the corresponding module from that file
for file_name in glob.glob(f"{Path(__file__).parent}/board/*.py"):
    module_name = Path(file_name).stem 
    if module_name.lower().replace("_", "").replace("-", "") in board_name.lower().replace("_", "").replace("-", ""):
        # Try to import the module from the file
        try:
            import importlib
            board_module = importlib.import_module(f".board.{module_name}", package='seeed_python_rpi')
            board_class = getattr(board_module, module_name)
            break
        except ImportError:
            print(f"Failed to load board module {module_name}")

class _Core(board_class):
    def list_leds(self):
        leds = []
        for f in glob.glob(_Core.STA_LED_DIR+"/*"):
            if not f.endswith("brightness"):
                leds.append(f[len(_Core.STA_LED_DIR) + 1 :])
        return leds
    
    def set_led(self, name):
        if name not in self.list_leds:
            raise ValueError("Invalid LED name.")
        self.__write_to_file(_Core.STA_LED_DIR + "/" + name + "/brightness", "1")
        
    def clean_led(self, name):
        if name not in self.list_leds:
            raise ValueError("Invalid LED name.")
        self.__write_to_file(_Core.STA_LED_DIR + "/" + name + "/brightness", "0")
        
    @property
    def sta_led(self):
        return self.sta_led_green

    @sta_led.setter
    def sta_led(self, value):
        self.sta_led_green = value
        self.sta_led_red = False

    @property
    def sta_led_green(self):
        if not hasattr(_Core, 'STA_LED_GREEN_BRIGHTNESS'):
            raise AttributeError("No Green LED found on this platform.")
        return True if self.__read_1st_line_from_file(_Core.STA_LED_GREEN_BRIGHTNESS) != "0" else False

    @sta_led_green.setter
    def sta_led_green(self, value):
        if not hasattr(_Core, 'STA_LED_GREEN_BRIGHTNESS'):
            raise AttributeError("No Green LED found on this platform.")
        self.__write_to_file(_Core.STA_LED_GREEN_BRIGHTNESS, "1" if value else "0")

    @property
    def sta_led_red(self):
        if not hasattr(_Core, 'STA_LED_RED_BRIGHTNESS'):
            raise AttributeError("No Red LED found on this platform.")
        return True if self.__read_1st_line_from_file(_Core.STA_LED_RED_BRIGHTNESS) != "0" else False

    @sta_led_red.setter
    def sta_led_red(self, value):
        if not hasattr(_Core, 'STA_LED_RED_BRIGHTNESS'):
            raise AttributeError("No Red LED found on this platform.")
        self.__write_to_file(_Core.STA_LED_RED_BRIGHTNESS, "1" if value else "0")

    @property
    def sta_led_blue(self):
        if not hasattr(_Core, 'STA_LED_BLUE_BRIGHTNESS'):
            raise AttributeError("No Blue LED found on this platform.")
        return True if self.__read_1st_line_from_file(_Core.STA_LED_BLUE_BRIGHTNESS) != "0" else False

    @sta_led_blue.setter
    def sta_led_blue(self, value):
        if not hasattr(_Core, 'STA_LED_BLUE_BRIGHTNESS'):
            raise AttributeError("No Blue LED found on this platform.")
        self.__write_to_file(_Core.STA_LED_BLUE_BRIGHTNESS, "1" if value else "0")
        
    @property
    def usr_led(self):
        if not hasattr(_Core, 'USR_LED_0_BRIGHTNESS'):
            raise AttributeError("No user LED found on this platform.")
        return True if self.__read_1st_line_from_file(_Core.USR_LED_0_BRIGHTNESS) != "0" else False

    @usr_led.setter
    def usr_led(self, value):
        if not hasattr(_Core, 'USR_LED_0_BRIGHTNESS'):
            raise AttributeError("No user LED found on this platform.")
        self.__write_to_file(_Core.USR_LED_0_BRIGHTNESS, "1" if value else "0")

    @property
    def buzzer(self):
        if hasattr(_Core, 'BUZZER_BRIGHTNESS'):
            return True if self.__read_1st_line_from_file(_Core.BUZZER_BRIGHTNESS) != "0" else False
        elif hasattr(_Core, 'BUZZER_GPIO_CHIP'):
            chip = gpiod.Chip(_Core.BUZZER_GPIO_CHIP)
            line = chip.find_lines(_Core.BUZZER_GPIO_LINE)
            if line is not None:
                return True if line.get_value() == 1 else False
        else:
            raise AttributeError("No buzzer found on this platform.")

    @buzzer.setter
    def buzzer(self, value):
        if hasattr(_Core, 'BUZZER_BRIGHTNESS'):
            self.__write_to_file(_Core.BUZZER_BRIGHTNESS, "1" if value else "0")
        elif hasattr(_Core, 'BUZZER_GPIO_CHIP'):
            chip = gpiod.Chip(_Core.BUZZER_GPIO_CHIP)
            line = chip.get_line(_Core.BUZZER_GPIO_LINE)
            if line is not None:
                line.request(consumer="gpio", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
                line.set_value(1 if value else 0)
        else:
            raise AttributeError("No buzzer found on this platform.")
        
    @property
    def illuminance(self):
        return int(self.__read_1st_line_from_file(_Core.LIGHT_ILLUMINANCE))

    @property
    def fan(self):
        if hasattr(_Core, '__FAN_GPIO_CHIP'):
            chip = gpiod.Chip(_Core.FAN_GPIO_CHIP)
            line = chip.get_line(label=_Core.FAN_GPIO_LINE)
            if line is not None:
                return True if line.get_value() == 1 else False
        else:
            raise AttributeError("No fan found on this platform.")

    @fan.setter
    def fan(self, value):
        if hasattr(_Core, '__FAN_GPIO_CHIP'):
            chip = gpiod.Chip(_Core.FAN_GPIO_CHIP)
            line = chip.get_line(label=_Core.FAN_GPIO_LINE)
            if line is not None:
                line.request(consumer="gpio", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
                line.set_value(1 if value else 0)
        else:
            raise AttributeError("No fan found on this platform.")

    @property
    def rs232_or_rs485(self):
        return _Core.RS232_OR_RS485 

    @rs232_or_rs485.setter
    def rs232_or_rs485(self, value):
        if hasattr(_Core, '__RS485_TX_RX_SWITCH_GPIO_CHIP'):
            chip = gpiod.Chip(_Core.RS232_OR_RS485_SWITCH_GPIO_CHIP)
            line = chip.find_lines(label=_Core.RS232_OR_RS485_SWITCH_GPIO_LINE)[0]
            if chip.find_lines(label=_Core.RS232_OR_RS485_SWITCH_GPIO_LINE) is not None:
                if value == "RS232":
                    line.request(consumer="gpio", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
                    line.set_value(0)
                    _Core.RS232_OR_RS485 = "RS232" 
                elif value == "RS485":
                    line.request(consumer="gpio", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
                    line.set_value(1)
                    _Core.RS232_OR_RS485 = "RS485" 
                else:
                    print('rs232/rs485 select input param error.please use "RS232" or "RS485"')

    @property
    def rs485_tx_rx_stat(self):
        return _Core.RS485_TX_RX_STAT

    @rs485_tx_rx_stat.setter
    def rs485_tx_rx_stat(self, value):
        if hasattr(_Core, '__RS485_TX_RX_SWITCH_GPIO_CHIP'):
            chip = gpiod.Chip(_Core.RS485_TX_RX_SWITCH_GPIO_CHIP)
            line = chip.find_lines(label=_Core.RS485_TX_RX_SWITCH_GPIO_LINE)[0]
            if chip.find_lines(label=_Core.RS485_TX_RX_SWITCH_GPIO_LINE) is not None:
                
                if value == "TX":
                    line.request(consumer="gpio", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
                    line.set_value(1)
                    _Core.RS485_TX_RX_STAT = "TX" 
                elif value == "RX":
                    line.request(consumer="gpio", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
                    line.set_values(0)
                    _Core.RS485_TX_RX_STAT = "RX" 
                else:
                    print('rs485 stat switch input param error.please use "TX" or "RX"')

    def __read_1st_line_from_file(self, file_name):
        with open(file_name, "r") as f:
            return f.readline().replace("\n", "")

    def __write_to_file(self, file_name, value):
        with open(file_name, "w") as f:
            f.write(value)

    def __get_event_device_path(self, name):
        file_name_list = glob.glob(_Core.EVENT_CLASS_PATH + "*")

        for file_name in file_name_list:
            event_num = file_name[len(_Core.EVENT_CLASS_PATH):]
            with open(f"{_Core.EVENT_CLASS_PATH}{event_num}/device/name") as f:
                device_name = f.readline().replace("\n", "")
                if device_name == name:
                    return _Core.EVENT_DEVICE_PATH + event_num

    def __get_button_device_path(self):
        return self.__get_event_device_path(_Core.BUTTON_DEVICE_NAME)

    def __get_acceleration_device_path(self):
        return self.__get_event_device_path(_Core.ACCELERATION_DEVICE_NAME)

    def get_button_device(self):
        return evdev.InputDevice(self.__get_button_device_path())

    def get_acceleration_device(self):
        return evdev.InputDevice(self.__get_acceleration_device_path())


sys.modules[__name__] = _Core()
