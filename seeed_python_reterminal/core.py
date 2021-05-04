import sys
import glob
import evdev


class _Core:

    __STA_LED_GREEN_BRIGHTNESS = "/sys/class/leds/usr_led2/brightness"
    __STA_LED_RED_BRIGHTNESS = "/sys/class/leds/usr_led1/brightness"
    __USR_LED_GREEN_BRIGHTNESS = "/sys/class/leds/usr_led0/brightness"
    __BUZZER_BRIGHTNESS = "/sys/class/leds/usr_buzzer/brightness"

    __EVENT_CLASS_PATH = "/sys/class/input/event"
    __EVENT_DEVICE_PATH = "/dev/input/event"
    __BUTTON_DEVICE_NAME = "gpio_keys"
    __ACCELERATION_DEVICE_NAME = "ST LIS3LV02DL Accelerometer"

    @property
    def sta_led(self):
        return self.sta_led_green

    @sta_led.setter
    def sta_led(self, value):
        self.sta_led_green = value
        self.sta_led_red = False

    @property
    def sta_led_green(self):
        return True if self.__read_1st_line_from_file(_Core.__STA_LED_GREEN_BRIGHTNESS) != "0" else False

    @sta_led_green.setter
    def sta_led_green(self, value):
        self.__write_to_file(_Core.__STA_LED_GREEN_BRIGHTNESS, "1" if value else "0")

    @property
    def sta_led_red(self):
        return True if self.__read_1st_line_from_file(_Core.__STA_LED_RED_BRIGHTNESS) != "0" else False

    @sta_led_red.setter
    def sta_led_red(self, value):
        self.__write_to_file(_Core.__STA_LED_RED_BRIGHTNESS, "1" if value else "0")

    @property
    def usr_led(self):
        return True if self.__read_1st_line_from_file(_Core.__USR_LED_GREEN_BRIGHTNESS) != "0" else False

    @usr_led.setter
    def usr_led(self, value):
        self.__write_to_file(_Core.__USR_LED_GREEN_BRIGHTNESS, "1" if value else "0")

    @property
    def buzzer(self):
        return True if self.__read_1st_line_from_file(_Core.__BUZZER_BRIGHTNESS) != "0" else False

    @buzzer.setter
    def buzzer(self, value):
        self.__write_to_file(_Core.__BUZZER_BRIGHTNESS, "1" if value else "0")

    def __read_1st_line_from_file(self, file_name):
        with open(file_name, "r") as f:
            return f.readline().replace("\n", "")

    def __write_to_file(self, file_name, value):
        with open(file_name, "w") as f:
            f.write(value)

    def __get_event_device_path(self, name):
        file_name_list = glob.glob(_Core.__EVENT_CLASS_PATH + "*")

        for file_name in file_name_list:
            event_num = file_name[len(_Core.__EVENT_CLASS_PATH):]
            with open(f"{_Core.__EVENT_CLASS_PATH}{event_num}/device/name") as f:
                device_name = f.readline().replace("\n", "")
                if device_name == name:
                    return _Core.__EVENT_DEVICE_PATH + event_num

    def __get_button_device_path(self):
        return self.__get_event_device_path(_Core.__BUTTON_DEVICE_NAME)

    def __get_acceleration_device_path(self):
        return self.__get_event_device_path(_Core.__ACCELERATION_DEVICE_NAME)

    def get_button_device(self):
        return evdev.InputDevice(self.__get_button_device_path())

    def get_acceleration_device(self):
        return evdev.InputDevice(self.__get_acceleration_device_path())


sys.modules[__name__] = _Core()
