"""
Ping Pong Pi
Nat Zimmermann
github.com/natzim/PingPongPi

A basic object-oriented ping pong score tracker
"""


class Player:
    points = 0
    games_won = 0

    def __init__(self, name):
        self.name = name

    def win_game(self):
        print("%s wins the game!" % self.name)
        self.games_won += 1
        self.points = 0
        self.opponent.points = 0

    def win_match(self):
        print("%s wins the match! Starting new match..." % self.name)
        Match()


class Match:
    points_to_win = 11
    games_to_win = 2
    serve_turns = 2
    deuce = False

    def __init__(self):
        self.player1 = Player(input("Player 1 name: "))
        self.player2 = Player(input("Player 2 name: "))

        self.player1.opponent = self.player2
        self.player2.opponent = self.player1

        self.first_server = input("First server (1/2): ")

        if self.first_server is "1":
            self.first_server = self.player1
        elif self.first_server is "2":
            self.first_server = self.player2
        else:
            raise ValueError()

        self.current_server = self.first_server

        self.user_control()

    def check_score(self):
        print_score = True
        swap_servers = True

        for player in [self.player1, self.player2]:
            if self.deuce:
                if player.points - player.opponent.points is 2:
                    player.win_game()
                    self.deuce = False
                    self.serve_turns = 2
                    self.current_server = self.first_server.opponent
                    self.first_server = self.current_server
                    swap_servers = False
            else:
                if (player.points is self.points_to_win - 1 and
                        player.opponent.points is self.points_to_win - 1):
                    self.deuce = True
                    self.serve_turns = 1
                if player.points is self.points_to_win:
                    player.win_game()
                    self.deuce = False
                    self.current_server = self.first_server.opponent
                    self.first_server = self.current_server
                    swap_servers = False
                if player.games_won is self.games_to_win:
                    player.win_match()
                    print_score = False

        if print_score:
            if ((self.player1.points + self.player2.points)
                    % self.serve_turns is 0 or
                    self.player1.points + self.player2.points is 0):
                if swap_servers:
                    self.current_server = self.current_server.opponent

                print("%s is serving next!" % self.current_server.name)

        return print_score

    def print_score(self):
        print("Name | P | G")
        for player in [self.player1, self.player2]:
            print("%s | %d | %d" % (player.name, player.points,
                                    player.games_won))

    def user_control(self):
        command = input("Command: ")
        command_recognised = True

        if command is "1":
            self.player1.points += 1
        elif command is "2":
            self.player2.points += 1
        else:
            print("Command not recognised")
            command_recognised = False

        if command_recognised and self.check_score():
            self.print_score()

        self.user_control()

Match()
