""" Class for the KPC Agent """

import re

from keypad import Keypad
from leds import Leds
from GPIOSimulator_v5 import GPIOSimulator


class KPCAgent:
    """ Class for the KPC Agent """

    def __init__(self, keypad: Keypad, led_board: Leds,
                 l_id: int = 0, l_dur: int = 0) -> None:
        self.keypad = keypad
        self.led_board = led_board
        self.password_path = './password_file.txt'
        self.override_signal = ""
        self.passcode_buffer = ""
        self.new_passcode = ""
        self.l_id = l_id
        self.l_dur = l_dur

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
                'symbol': self.override_signal,
                'duration': 0
            }
            self.override_signal = ""  # Resetting the signal before returning
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

    def validate_passcode_change(self, _signal):
        """ Check that new password is legal """
        target = "^[0-9]*$"
        if len(self.passcode_buffer) < 4 or re.match(
                target, self.passcode_buffer) is None:
            self.override_signal = "n"
        else:
            self.new_passcode = self.passcode_buffer
        self.passcode_buffer = ""

    def validate_and_write_new_passcode(self, _signal):
        print(self.passcode_buffer, self.new_passcode)
        if self.passcode_buffer == self.new_passcode:
            with open(self.password_path, 'w') as password_file:
                password_file.write(self.new_passcode)
            print("Successfully changed password")
        else:
            print("Passwords didn't match")

    def set_l_id(self, l_id):
        self.l_id = int(l_id)

    def light_one_led(self, _signal):
        """ Light the correct LED for the correct amount of time """
        self.l_dur = int(self.passcode_buffer)
        self.passcode_buffer = ""   # Resetting the buffer
        pattern = [[[0] * 6, self.l_dur]]
        pattern[0][0][self.l_id] = 1
        self.led_board.pattern(pattern)

    def flash_leds(self, _signal):
        """ Flash all LEDs on the LED Board """
        self.led_board.powering_up()

    def twinkle_leds(self):
        """ Twinkle all LEDs on the LED Board """
        self.led_board.login()

    def exit_action(self, _signal):
        """ Call LED Board to initiate power down lighting sequence """
        self.led_board.logout()


def main():

    my_gpio_simulator = GPIOSimulator()
    my_keypad = Keypad(my_gpio_simulator)
    my_ledboard = Leds(my_gpio_simulator)

    my_agent = KPCAgent(my_keypad, my_ledboard, "override")
    # login_result = my_agent.verify_login("jarlerul123")
    # print(f"Password match: {login_result}")

    new_passcode = "12399"
    new_passcode_result = my_agent.validate_passcode_change(new_passcode)
    print(new_passcode_result)


if __name__ == "__main__":
    main()
