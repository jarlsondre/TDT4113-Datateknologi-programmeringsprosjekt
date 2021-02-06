
""" This is my rock-paper-scissors program """

import random

actions = ["Playing Rock", "Playing Scissors", "Playing Paper"]


class Action:

    def __init__(self, index):
        self.actions = ["Playing Rock", "Playing Scissors", "Playing Paper"]
        self.action = self.actions[index]
        self.index = index

    def __eq__(self, other):
        return self == other

    def __gt__(self, other):
        return (self.index + 1) % 3 == other.index

    def __str__(self):
        return self.action


class Player:

    def __init__(self, name, type):
        self._enter_name(name)
        self.action = None
        self.won = None
        self.results = []
        self.type = type

    def _enter_name(self, name):
        self.name = name

    def receive_result(self, result):
        self.results.append(result)

    def __str__(self):
        return self.name + "(" + self.type + ")"


class Random(Player):

    def __init__(self, name):
        super().__init__(name, "Random")

    def select_action(self):
        self.action = Action(random.randint(0, 2))


class Sequential(Player):

    def __init__(self, name):
        super().__init__(name, "Sequential")
        self.counter = random.randint(0, 2)

    def select_action(self):
        self.action = Action(self.counter)
        self.counter = (self.counter + 1) % 3


class MostCommon(Player):
    def __init__(self, name):
        super().__init__(name, "Most Common")

    def select_action(self):
        if len(self.results) == 0:
            self.action = Action(random.randint(0, 2))
        else:  # Vi må telle antall forekomster av trekkene til motstanderen
            countingDict = {}
            for result in self.results:  # Teller antall forekomster
                countingDict[result[1].action] = countingDict.get(
                    result[1].action, 0) + 1
            highest_occurence = 0
            most_common = ""
            for key in countingDict:
                if countingDict[key] > highest_occurence:
                    highest_occurence = countingDict[key]
                    most_common = key
            self.action = Action((actions.index(most_common) + 2) % 3)



class Historian(Player):
    def __init__(self, name, remember = 1):
        super().__init__(name, "Historian" + "(" + str(remember) + ")")
        self.remember = remember

    def select_action(self):
        if len(self.results) < self.remember + 1:
            self.action = Action(random.randint(0, 2))
        else:
            opponent_moves = []
            for result in self.results:
                opponent_moves.append(result[1].action)
            last_opponent_moves = []
            for i in range(-self.remember, 0): # Finner de siste trekkene avhengig av hvor stor remember er
                last_opponent_moves.append(self.results[i][1].action)
            historian_counting_dict = {}
            for i in range(len(opponent_moves) - self.remember): # Teller antall forekomster
                matches = True
                for j in range(self.remember):
                    if opponent_moves[i + j] != last_opponent_moves[0 + j]:
                        matches = False
                        break
                if matches:
                    historian_counting_dict[opponent_moves[i + self.remember]] = historian_counting_dict.get(opponent_moves[i+self.remember], 0) + 1
            highest_occurence = 0
            highest_occuring_move = ""
            for key in historian_counting_dict:
                if historian_counting_dict[key] > highest_occurence:
                    highest_occurence = historian_counting_dict[key]
                    highest_occuring_move = key
            if len(historian_counting_dict) == 0:
                self.action = Action(random.randint(0, 2))
            else:
                self.action = Action((actions.index(highest_occuring_move) + 2) % 3)


