"""
Ping Pong Pi
Nat Zimmermann
github.com/natzim/PingPongPi

A basic object-oriented ping pong score tracker
"""

import sqlite3


class Player:
    points = 0
    total_points = 0
    games_won = 0

    def __init__(self, name):
        self.name = name

    def add_point(self):
        self.points += 1
        self.total_points += 1

    def win_game(self):
        print("%s wins the game!" % self.name)
        self.games_won += 1
        self.points = 0
        self.opponent.points = 0

    def win_match(self):
        print("%s wins the match! Adding to database..." % self.name)

        conn = sqlite3.connect("pingpong.db")

        conn.execute("""create table if not exists matches
                        (id integer primary key,
                        p1name text, p2name text,
                        p1points int, p2points int,
                        p1games int, p2games int)""")

        conn.execute("""insert into matches
                        (p1name, p2name, p1points, p2points, p1games, p2games)
                        values (?, ?, ?, ?, ?, ?)""",
                        (self.name, self.opponent.name, self.total_points,
                         self.opponent.total_points, self.games_won,
                         self.opponent.games_won))

        conn.commit()
        conn.close()

        print("Match added to database! Starting new match...")
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
            self.player1.add_point()
        elif command == "2":
            self.player2.add_point()
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
