
import itertools as it
import time

import GPIOSimulator_v5 as GPIO


class Leds:
    """Interface to the leds"""

    def __init__(self, gpio_instance: GPIO.GPIOSimulator) -> None:
        self.leds = [
            ('H', 'L', 'I'),  # led0
            ('L', 'H', 'I'),  # led1
            ('I', 'H', 'L'),  # led2
            ('I', 'L', 'H'),  # led3
            ('H', 'I', 'L'),  # led4
            ('L', 'I', 'H'),  # led5
        ]
        self.gpio = gpio_instance

    def turn_on_led(self, led: int) -> None:
        """
        Turn on a led indexed 0 through 5.
        """
        for pin, state in enumerate(self.leds[led]):
            if state == 'H':
                self.gpio.setup(pin, self.gpio.OUT)
                self.gpio.output(pin, self.gpio.HIGH)
            elif state == 'L':
                self.gpio.setup(pin, self.gpio.OUT)
                self.gpio.output(pin, self.gpio.LOW)
            elif state == 'I':
                self.gpio.setup(pin, self.gpio.IN)
            else:
                raise ValueError(f'Undefined state: {state}')

    def turn_off_leds(self):
        """Turn off all the leds"""
        self.gpio.setup(0, self.gpio.IN)
        self.gpio.setup(1, self.gpio.IN)
        self.gpio.setup(2, self.gpio.IN)

    def powering_up(self):
        """Sequence to be displayed when powering up"""
        self.pattern([[[1]*6, 1]])

    def wrong_password(self):
        """Sequence to be displayed when the user enters a wrong password"""
        self.pattern([it.repeat([[1]*6, 0.3, [0]*6, 0.3], 4)])

    def login(self):
        """Sequence to be displayed when the user in grated access"""
        self.pattern([[[1, 0, 0, 0, 0, 0][-i:] + [1, 0, 0, 0, 0, 0][:-i], 0.15] for i in range(6)])

    def logout(self):
        """Sequence to be displayed when the user logs out"""
        pattern = [[[1, 0, 0, 0, 0, 0][-i:] + [1, 0, 0, 0, 0, 0][:-i], 0.15] for i in range(6)]
        self.pattern(list(reversed(pattern)))

    def pattern(self, pattern: list) -> None:
        for states, sleep in pattern:
            for led, state in enumerate(states):
                if state:
                    self.turn_on_led(led)
            self.show()
            time.sleep(sleep)
            self.turn_off_leds()

    def show(self):
        self.gpio.show_leds_states()