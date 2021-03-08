from kpc_agent import KPCAgent
from rule import Rule

class FSM:
    """ Class for the finite state machine """

    def __init__(self, agent: KPCAgent) -> None:
        self.state = 'START'
        self.agent = agent
        self.rules = []

    def add_rule(self, rule: Rule):
        """ Add a new rule to end of the FSM's rule list """
        self.rules.append(rule)

    def get_next_signal(self):
        """ Query the agent for the next signal """
        pass

    def run(self, START, END):
        """ Begin in the initial state and then
        repeatedly call get_next_signal until reaching the final state """
        self.state = START
        while self.state != END:
            signal = self.agent.get_next_signal()
            for rule in self.rules:
                if rule.match(self.state, signal['symbol']):
                    rule.action(signal['symbol'])
                    self.state = rule.give_new_state()
                    break

