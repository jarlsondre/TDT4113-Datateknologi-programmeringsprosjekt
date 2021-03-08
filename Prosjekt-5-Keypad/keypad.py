"""
Interface to the keypad
"""
import itertools as it
import time

import GPIOSimulator_v5 as GPIO


class Keypad:
    """
    Interface to the keypad
    """

    def __init__(self, gpio: GPIO.GPIOSimulator,
                 polling_rate_hz: int = 50) -> None:
        self.gpio = gpio
        self.polling_rate_hz = polling_rate_hz
        self.cols = [
            GPIO.PIN_KEYPAD_COL_0,
            GPIO.PIN_KEYPAD_COL_1,
            GPIO.PIN_KEYPAD_COL_2]
        self.rows = [GPIO.PIN_KEYPAD_ROW_0, GPIO.PIN_KEYPAD_ROW_1,
                     GPIO.PIN_KEYPAD_ROW_2, GPIO.PIN_KEYPAD_ROW_3]
        self.mapping = {
            (rc[0], rc[1]): ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'][i]
            for i, rc in enumerate(it.product(self.rows, self.cols))}
        self.setup_gpio()

    def setup_gpio(self):
        """
        Configures the pins to the keypad
        """
        for pin in self.rows:
            self.gpio.setup(pin, self.gpio.OUT)
        for pin in self.cols:
            self.gpio.setup(pin, self.gpio.IN, self.gpio.LOW)

    def read(self):
        """
        Read a single symbol from the keypad and returns the symbol and click duration
        :return: {
            'symbol': str,
            'duration': float
        }
        """
        row, col = self.read_row_col()
        click_time = time.time()
        self.gpio.output(row, self.gpio.HIGH)
        while self.gpio.input(col):
            time.sleep(1 / self.polling_rate_hz)
        self.gpio.output(row, self.gpio.LOW)
        return {
            'symbol': self.mapping[(row, col)],
            'duration': time.time() - click_time
        }

    def read_row_col(self):
        """
        Returns the row and column of a active cell.
        :return: row, col
        """
        while True:
            time.sleep(1 / self.polling_rate_hz)
            for row in self.rows:
                self.gpio.output(row, self.gpio.HIGH)
                for col in self.cols:
                    if self.gpio.input(col):
                        self.gpio.output(row, self.gpio.LOW)
                        return row, col
                self.gpio.output(row, self.gpio.LOW)
