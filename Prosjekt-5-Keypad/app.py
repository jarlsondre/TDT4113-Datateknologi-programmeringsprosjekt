
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
agent = KPCAgent(keypad, leds)
fsm = FSM(agent)


rules = [
    Rule(  # A1
        current=State.START,
        next=State.INPUT_PASSWORD,
        signal=Rule.signal_is_any,
        action=fsm.agent.flash_leds
    ), Rule(  # A2
        current=State.INPUT_PASSWORD,
        next=State.INPUT_PASSWORD,
        signal=Rule.signal_is_digit,
        action=fsm.agent.write_symbol_to_buffer
    ), Rule(  # A3
        current=State.INPUT_PASSWORD,
        next=State.CHECK_PASSWORD,
        signal=Rule.signal_is_specific('*'),
        action=fsm.agent.verify_login
    ), Rule(  # A4
        current=State.INPUT_PASSWORD,
        next=State.START,
        signal=Rule.signal_is_any,
        action=fsm.agent.reset_passcode_entry
    ), Rule(  # A5
        current=State.CHECK_PASSWORD,
        next=State.MENY,
        signal=Rule.signal_is_specific('y'),
        action=fsm.agent.clear_buffer
    ), Rule(  # A4
        current=State.CHECK_PASSWORD,
        next=State.START,
        signal=Rule.signal_is_any,
        action=fsm.agent.clear_buffer
    ), Rule(  # A1
        current=State.MENY,
        next=State.INPUT_NEW_PASSWORD,
        signal=Rule.signal_is_specific('*'),
        action=fsm.agent.reset_passcode_entry
    ), Rule(  # SET LED ID
        current=State.MENY,
        next=State.LED_DURATION,
        signal=Rule.signal_is_led_number,
        action=fsm.agent.set_l_id
    ), Rule(  # SET LED DURATION
        current=State.LED_DURATION,
        next=State.LED_DURATION,
        signal=Rule.signal_is_digit,
        action=fsm.agent.write_symbol_to_buffer
    ), Rule(  # TURN ON LED
        current=State.LED_DURATION,
        next=State.MENY,
        signal=Rule.signal_is_specific('*'),
        action=fsm.agent.light_one_led
    ), Rule(  # LED DURATION WRONG INPUT
        current=State.LED_DURATION,
        next=State.MENY,
        signal=Rule.signal_is_any,
        action=fsm.agent.reset_passcode_entry
    ), Rule(  # CONFIRM LOGOUT
        current=State.MENY,
        next=State.CONFIRM_LOGOUT,
        signal=Rule.signal_is_specific('#'),
        action=fsm.agent.clear_buffer
    ), Rule(  # LOGOUT
        current=State.CONFIRM_LOGOUT,
        next=State.START,
        signal=Rule.signal_is_specific('#'),
        action=fsm.agent.exit_action
    ), Rule(  # LOGOUT CANCELLED
        current=State.CONFIRM_LOGOUT,
        next=State.MENY,
        signal=Rule.signal_is_any,
        action=fsm.agent.clear_buffer
    ), Rule(  # A2
        current=State.INPUT_NEW_PASSWORD,
        next=State.INPUT_NEW_PASSWORD,
        signal=Rule.signal_is_digit,
        action=fsm.agent.write_symbol_to_buffer
    ), Rule(  # A7
        current=State.INPUT_NEW_PASSWORD,
        next=State.VALIDATE_NEW_PASSWORD,
        signal=Rule.signal_is_specific('*'),
        action=fsm.agent.validate_passcode_change
    ), Rule(  # A6
        current=State.INPUT_NEW_PASSWORD,
        next=State.MENY,
        signal=Rule.signal_is_any,
        action=fsm.agent.reset_passcode_entry
    ), Rule(  # A2
        current=State.VALIDATE_NEW_PASSWORD,
        next=State.VALIDATE_NEW_PASSWORD,
        signal=Rule.signal_is_digit,
        action=fsm.agent.write_symbol_to_buffer
    ), Rule(  # A7
        current=State.VALIDATE_NEW_PASSWORD,
        next=State.MENY,
        signal=Rule.signal_is_specific('*'),
        action=fsm.agent.validate_and_write_new_passcode
    ), Rule(  # A6
        current=State.VALIDATE_NEW_PASSWORD,
        next=State.MENY,
        signal=Rule.signal_is_any,
        action=fsm.agent.reset_passcode_entry
    )
]

for rule in rules:
    fsm.add_rule(rule)

fsm.run(State.START, State.END)
