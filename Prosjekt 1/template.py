""" Template for Project 1: Morse code """
import time
from GPIOSimulator_v1 import *

GPIO = GPIOSimulator()

MORSE_CODE = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
              '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
              '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
              '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
              '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
              '---..': '8', '----.': '9', '-----': '0'}


class MorseDecoder():
    """ Morse code class """


    def __init__(self):
        """ initialize your class """
        self.time_variable = 0.3
        self.current_symbol = ""
        self.current_word = ""
        self.message = ""

    # Resetter symbolet
    def reset(self):
        """ reset the variable for a new run """
        self.current_symbol = ""

    # Finner neste signal
    def read_one_signal(self):
        """ read a signal from Raspberry Pi """

        # Finner det første signalet
        initial_signal = 0
        for i in range(4):
            initial_signal += GPIO.input(PIN_BTN)

        if initial_signal > 2:
            initial_signal = 1
        else:
            initial_signal = 0

        # Sjekker hvor lenge signalet varer og returnerer tilsvarende verdi
        start_time = time.time()
        counter = 0
        if initial_signal == 1:
            while counter < 3:  # For å gjøre feilen usannsynlig så signalet endres tre ganger på rad
                signal = GPIO.input(PIN_BTN)
                if signal == 0:
                    counter += 1
                else:
                    counter = 0
            signal_time = time.time() - start_time
            if signal_time > self.time_variable*3:
                return "-"
            elif signal_time > self.time_variable:
                return "."
            else:
                return ""
        else:
            while counter < 3:
                signal = GPIO.input(PIN_BTN)
                if signal == 1:
                    counter += 1
                else:
                    counter = 0
            signal_time = time.time() - start_time
            if signal_time > self.time_variable*7:
                return "3"
            elif signal_time > self.time_variable*4.5:
                return "2"
            else:
                return ""


    def decoding_loop(self):
        """ the main decoding loop """

        while True:  # Henter signaler kontinuerlig
            self.process_signal(self.read_one_signal())


    # Kaller riktig metode avhengig av om det er pause eller ikke
    def process_signal(self, signal):
        """ handle the signals using corresponding functions """
        if signal == "-" or signal == ".":
            self.update_current_symbol(signal)
        elif signal == "2":
            self.handle_symbol_end()
        elif signal == "3":
            self.handle_word_end()


    def update_current_symbol(self, signal):
        """ append the signal to current symbol code """
        self.current_symbol += signal
        # Blinker med lysene avhengig av om det er dot eller dash
        if signal == ".":
            GPIO.output(PIN_RED_LED_0, GPIO.HIGH)
            GPIO.output(PIN_RED_LED_1, GPIO.HIGH)
            GPIO.output(PIN_RED_LED_2, GPIO.HIGH)
            GPIO.output(PIN_RED_LED_0, GPIO.LOW)
            GPIO.output(PIN_RED_LED_1, GPIO.LOW)
            GPIO.output(PIN_RED_LED_2, GPIO.LOW)
        else:
            GPIO.output(PIN_BLUE_LED, GPIO.HIGH)
            GPIO.output(PIN_BLUE_LED, GPIO.LOW)


    def handle_symbol_end(self):
        """ process when a symbol ending appears """
        # Sjekker om bokstaven finnes. Dersom den ikke finnes så forsvinner den bare
        if self.current_symbol in MORSE_CODE:
            self.current_word += MORSE_CODE[self.current_symbol]
        self.reset()


    def handle_word_end(self):
        """ process when a word ending appears """
        # Legger til ordet og resetter
        self.handle_symbol_end()
        if self.current_word != "":
            self.message += self.current_word + " "
        self.show_message()
        self.current_word = ""


    def handle_reset(self):
        """ process when a reset signal received """


    def show_message(self):
        """ print the decoded message """
        print(self.message)


def main():
    """ the main function """
    decoder = MorseDecoder()
    decoder.decoding_loop()


if __name__ == "__main__":
    main()
