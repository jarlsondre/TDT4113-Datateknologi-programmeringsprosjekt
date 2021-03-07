from typing import Callable

class Rule:
    """ Class for Rules that can be stored within an FSM """
    def __init__(self, trigger_state, signal_match: Callable, new_state, action: Callable) -> None:
        self.trigger_state = trigger_state
        self.signal_match = signal_match
        self.new_state = new_state
        self.action = action

    def match(self, current_state, signal):
        """ Check whether the rule condition is fulfillled """
        return current_state is self.trigger_state and self.signal_match(signal)