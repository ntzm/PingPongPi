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

        self.set_first_server()

        self.user_control()

    def set_first_server(self):
        set_server = True

        self.first_server = input("First server (1/2): ")

        if self.first_server == "1":
            self.first_server = self.player1
        elif self.first_server == "2":
            self.first_server = self.player2
        else:
            print("Please enter either 1 or 2!")
            set_server = False
            self.set_first_server()

        if set_server:
            self.current_server = self.first_server

    def check_score(self):
        print_score = True
        swap_servers = True

        for player in [self.player1, self.player2]:
            if self.deuce:
                if player.points - player.opponent.points == 2:
                    player.win_game()
                    self.deuce = False
                    self.serve_turns = 2
                    self.current_server = self.first_server.opponent
                    self.first_server = self.current_server
                    swap_servers = False
            else:
                if (player.points == self.points_to_win - 1 and
                        player.opponent.points == self.points_to_win - 1):
                    self.deuce = True
                    self.serve_turns = 1
                if player.points == self.points_to_win:
                    player.win_game()
                    self.deuce = False
                    self.current_server = self.first_server.opponent
                    self.first_server = self.current_server
                    swap_servers = False
                if player.games_won == self.games_to_win:
                    player.win_match()
                    print_score = False

        if print_score:
            if ((self.player1.points + self.player2.points)
                    % self.serve_turns == 0 or
                    self.player1.points + self.player2.points == 0):
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
        print_score = True

        if command == "1":
            self.player1.points += 1
        elif command == "2":
            self.player2.points += 1
        elif command == "exit":
            exit()
        elif command == "settings":
            self.points_to_win = input("Points to win a game (%d): "
                                       % self.points_to_win)
            self.games_to_win = input("Games to win a match (%d): "
                                      % self.games_to_win)
            self.serve_turns = input("Serve truns (%d): " % self.serve_turns)
            print_score = False
        else:
            print("Command not recognised")
            print_score = False

        if print_score and self.check_score():
            self.print_score()

        self.user_control()

Match()
