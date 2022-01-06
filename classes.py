class Team:
    def __init__(self, name, seed, pool):
        self.name = name
        self.seed = seed
        self.pool = pool
        self.games = []
        self.rating = 1000
        self.game_ratings = []

    #allows sorting by seed
    def __lt__(self, other):
        return int(self.seed) < int(other.seed)

    def print_team(self):
        print("Team: " + self.name + " (" + self.seed + ")")

    def add_game(self, game):
        self.games.append(game)

    def print_games(self):
        self.print_team()
        for game in self.games:
            game.print_game()

class Game:
    def __init__(self, teamA, teamB, teamA_score, teamB_score, datetime, pool):
        self.teamA = teamA
        self.teamB = teamB
        self.teamA_score = teamA_score
        self.teamB_score = teamB_score
        self.datetime = datetime
        self.pool = pool

    #allows sorting by datetime
    def __lt__(self, other):
        return self.datetime < other.datetime

    def print_game(self):
        print("Game: " + str(self.datetime.strftime("%b %d %H:%M")) + " | " + self.teamA.name + " vs. " + self.teamB.name + ", " + self.teamA_score + " - " + self.teamB_score)
