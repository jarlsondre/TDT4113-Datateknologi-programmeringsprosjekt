""" Class for the FSM """


class FSM:
    """ Class for the finite state machine """

    def __init__(self):
        self.state = 0

    def add_rule(self):
        """ Add a new rule to end of the FSM's rule list """
        pass

    def get_next_signal(self):
        """ Query the agent for the next signal """
        pass

    def run(self):
        """ Begin in the initial state and then
        repeatedly call get_next_signal until reaching the final state """
        pass

    def match(self):
        """ Check whether the rule condition is fulfillled """
        pass

    def fire(self):
        """ use the consequent rule to set the next state of the FSM
        and call the appropriate agent action method """
        pass
