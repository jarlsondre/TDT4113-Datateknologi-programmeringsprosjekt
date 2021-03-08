""" Class for the KPC Agent """

import re

from keypad import Keypad
from leds import Leds
from GPIOSimulator_v5 import GPIOSimulator



class KPCAgent:
    """ Class for the KPC Agent """

    def __init__(self, keypad: Keypad, led_board: Leds, l_id: int = 0, l_dur: int = 0) -> None:
        self.keypad = keypad
        self.led_board = led_board
        self.password_path = './password_file.txt'
        self.override_signal = ""
        self.passcode_buffer = ""
        self.l_id = l_id
        self.l_dur = l_dur
        self.twinkle_time = 0.5  # Turns on the light for 0.5 seconds

    def write_symbol_to_buffer(self, char):
        """ Write a character to the password buffer """
        self.passcode_buffer += char

    def reset_passcode_entry(self, _signal):
        """ Clear passcode buffer and initiate a power up lighting sequence on the LED Board """
        self.passcode_buffer = ""
        self.led_board.powering_up()

    def get_next_signal(self):
        """ Query the next keypad for the next pressed key """
        if self.override_signal != "":
            return_value = {
                'symbol' : self.override_signal,
                'duration': 0
            }
            self.override_signal = "" # Resetting the signal before returning
            return return_value
        return self.keypad.read()

    def verify_login(self, *args) -> None:
        """ Check that the password entered matches password stored in file """
        with open(self.password_path, 'r') as password_file:
            password = password_file.readlines()[0]
        if password == self.passcode_buffer:
            self.led_board.login()
            self.override_signal = "y"
        else:
            self.override_signal = "n"

    def validate_passcode_change(self, new_passcode: str):
        """ Check that new password is legal """
        target = "^[0-9]*$"
        return not len(new_passcode) < 4 or re.match(
            target, new_passcode) is None

    def light_one_led(self):
        """ Light the correct LED for the correct amount of time """
        pattern = [[0] * 6, self.l_dur]
        pattern[0][self.l_id] = 1
        self.led_board.pattern(pattern)

    def flash_leds(self):
        """ Flash all LEDs on the LED Board """
        self.led_board.pattern([[1] * 6, 1])

    def twinkle_leds(self):
        """ Twinkle all LEDs on the LED Board """
        self.led_board.login()

    def exit_action(self, *args):
        """ Call LED Board to initiate power down lighting sequence """
        self.led_board.logout()


def main():

    my_gpio_simulator = GPIOSimulator()
    my_keypad = Keypad(my_gpio_simulator)
    my_ledboard = Leds(my_gpio_simulator)

    my_agent = KPCAgent(my_keypad, my_ledboard)

    new_passcode = "12399"
    new_passcode_result = my_agent.validate_passcode_change(new_passcode)
    print(new_passcode_result)

  


if __name__ == "__main__":
    main()
