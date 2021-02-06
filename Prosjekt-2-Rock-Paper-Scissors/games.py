
import players
from matplotlib import pyplot


class SingleGame:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.choice1 = None
        self.choice2 = None
        self.winner = None

    def perform_game(self):
        print("\nStarting the game!")
        self.player1.select_action()
        self.player2.select_action()
        self.choice1 = self.player1.action
        self.choice2 = self.player2.action
        if self.player1.action > self.player2.action:
            self.winner = self.player1
        elif self.player2.action > self.player1.action:
            self.winner = self.player2
        else:
            self.winner = None
        self.player1.receive_result([self.choice1, self.choice2, self.winner])
        self.player2.receive_result([self.choice2, self.choice1, self.winner])
        self.show_result()

    def show_result(self):
        print(
            f"{self.player1} chose {self.choice1} and {self.player2} chose {self.choice2}. The winner was {self.winner}")


class Tournament:

    def __init__(self, player1, player2, number_of_games):
        self.player1 = player1
        self.player2 = player2
        self.number_of_games = number_of_games

    def arrange_singlegame(self):
        game = SingleGame(self.player1, self.player2)
        game.perform_game()
        return [game.choice1, game.choice2, game.winner]

    def arrange_tournament(self):
        winner_list = []
        winner_dict = {}
        for i in range(self.number_of_games):
            results = self.arrange_singlegame()
            winner_dict[results[2].__str__()] = winner_dict.get(results[2].__str__(), 0) + 1
            winner_list.append(winner_dict.copy())
        ratio_list = []
        for i in range(self.number_of_games):
            if self.player1.__str__() in winner_list[i]:
                temp_ratio = winner_list[i][self.player1.__str__()] / (i + 1)
            else:
                temp_ratio = 0
            ratio_list.append(temp_ratio)
        pyplot.plot(ratio_list)
        pyplot.ylabel("ratio of wins for " + self.player1.name + " against " + self.player2.name)
        pyplot.xlabel("Games played")
        pyplot.axis([0, self.number_of_games, 0, 1])
        pyplot.hlines(0.5, 0, self.number_of_games, 'k', 'dashed')
        pyplot.show()




def main():
    first_player_name = input("What is player1's name? ")
    player1_type = input("Which player type is player 1? (R/M/S/H)")
    if player1_type == "H":
        depth = input("Which depth would like historian to remember?")
        player1 = players.Historian(first_player_name, int(depth))
    elif player1_type == "R":
        player1 = players.Random(first_player_name)
    elif player1_type == "M":
        player1 = players.MostCommon(first_player_name)
    else:
        player1 = players.Sequential(first_player_name)

    second_player_name = input("What is player2's name? ")
    player2_type = input("Which player type is player 2? (R/M/S/H)")

    if player2_type == "H":
        depth = input("Which depth would like historian to remember?")
        player2 = players.Historian(second_player_name, int(depth))
    elif player2_type == "R":
        player2 = players.Random(second_player_name)
    elif player2_type == "M":
        player2 = players.MostCommon(second_player_name)
    else:
        player2 = players.Sequential(second_player_name)
    tournament = Tournament(player1, player2, 30)
    tournament.arrange_tournament()

if __name__ == "__main__":
    main()
