from states import State
from typing import Any, Callable, Union
from inspect import isfunction



class Rule:
    """ Class for Rules that can be stored within an FSM """

    def __init__(self,
            current: State,
            next: Union[Callable, State],
            signal: Callable,
            action: Callable
    ) -> None:
        self.current = current
        self.signal = signal
        self.next = next
        self.action = action

    def match(self, current_state, signal):
        """ Check whether the rule condition is fulfillled """
        if current_state is self.current and self.signal(signal):
            print(", state =", current_state) 
        return current_state is self.current and self.signal(signal)

    def give_new_state(self):
        if isfunction(self.next):
            return self.next()
        return self.next

    @staticmethod
    def signal_is_digit(signal):
        return 48 <= ord(signal) <= 57

    @staticmethod
    def signal_is_led_number(signal):
        return 48 <= ord(signal) <= 53

    @staticmethod
    def signal_is_any(_signal):
        return True

    @staticmethod
    def signal_is_specific(char):
        def func(signal):
            return signal == char
        return func
