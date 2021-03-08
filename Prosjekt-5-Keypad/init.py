
from leds import Leds

from GPIOSimulator_v5 import GPIOSimulator as GPIO
from kpc_agent import KPCAgent
from keypad import Keypad
from fsm import FSM
from rule import Rule
from states import State

gpio = GPIO()
leds = Leds(gpio)
keypad = Keypad(gpio)
agent = KPCAgent(keypad, leds, '*')
fsm = FSM(agent)

def go_to_active_if_unlocked():
    if agent.fully_active:
        return State.MENY
    return State.START

rules = [
    Rule( # A1
        current=State.START,
        next=State.INPUT_PASSWORD,
        signal=Rule.signal_is_any,
        action=fsm.agent.reset_passcode_entry
    ), Rule( # A2
        current=State.INPUT_PASSWORD,
        next=State.INPUT_PASSWORD,
        signal=Rule.signal_is_digit,
        action=fsm.agent.write_symbol_to_buffer
    ), Rule( # A3
        current=State.INPUT_PASSWORD,
        next=State.CHECK_PASSWORD,
        signal=Rule.signal_is_specific('*'),
        action=fsm.agent.verify_login
    ),Rule( # A4
        current=State.INPUT_PASSWORD,
        next=State.START,
        signal=Rule.signal_is_any,
        action=fsm.agent.reset_passcode_entry
    ),Rule( # A5
        current=State.CHECK_PASSWORD,
        next=State.MENY,
        signal=Rule.signal_is_specific('y'),
        action=fsm.agent.reset_passcode_entry
    ),Rule( # A4
        current=State.CHECK_PASSWORD,
        next=State.START,
        signal=Rule.signal_is_any,
        action=fsm.agent.reset_passcode_entry
    ), Rule( # Finished, logging out
        current=State.MENY,
        next=State.END,
        signal=Rule.signal_is_any,
        action=fsm.agent.exit_action
    )
]

for rule in rules:
    fsm.add_rule(rule)

fsm.run(State.START, State.END)