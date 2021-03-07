from enum import Enum
from leds import Leds

from GPIOSimulator_v5 import GPIOSimulator as GPIO
from kpc_agent import KPCAgent
from keypad import Keypad
from fsm import FSM
from rule import Rule

gpio = GPIO()
leds = Leds(gpio)
keypad = Keypad(gpio)
agent = KPCAgent(keypad, leds, '*')
fsn = FSM(agent)

class State(Enum):
    START = 0
    INPUT_PASSWORD = 1
    CHECK_PASSWORD = 2
    END = 3

def signal_is_digit(signal):
    return 48 <= ord(signal) <= 57

def all_signals(signal):
    return True

def signal_is_specific(char):
    def func(signal):
        return signal == char
    return func

rules = [
    Rule(State.START, all_signals, State.INPUT_PASSWORD, fsn.agent.reset_passcode_entry),
    Rule(State.INPUT_PASSWORD, signal_is_digit, State.INPUT_PASSWORD, fsn.agent.write_to_passcode_buffer), 
    Rule(State.INPUT_PASSWORD, signal_is_specific('*'), State.START, fsn.agent.verify_login)
]

for rule in rules:
    fsn.add_rule(rule)

fsn.run(State.START, State.END)