""" Class for the KPC Agent """


class KPCAgent:
    """ Class for the KPC Agent """

    def __init__(self) -> None:
        self.keypad = None

    def reset_passcode_entry(self):
        """ Clear passcode buffer and initiate a power up lighting sequence on the LED Board """
        pass

    def get_next_signal(self):
        """ Query the next keypad for the next pressed key """
        pass

    def verify_login(self):
        """ Check that the password entered matches password stored in file """
        pass

    def validate_passcode_change(self):
        """ Check that new password is legal """
        pass

    def light_one_led(self):
        """ Light the correct LED for the correct amount of time """
        pass

    def flash_leds(self):
        """ Flash all LEDs on the LED Board """
        pass

    def twinkle_leds(self):
        """ Twinkle all LEDs on the LED Board """
        pass

    def exit_action(self):
        """ Call LED Board to initiate power down lighting sequence """
        pass
