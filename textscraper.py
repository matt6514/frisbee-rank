from datetime import datetime
from classes import Team, Game

#format:
# MM/DD/YYYY HH:MM AM/PM | TeamA (Seed) Score | TeamB (Seed) Score | *Round

def get_games(file, teams = None):
    games = []

    with open (file) as games_file:
        lines = games_file.readlines()

    for line in lines:
        if line == '\n':
            continue

        line = line.strip()
        parts = line.split('|')
        date_data = parts[0]
        teamA_data = parts[1]
        teamB_data = parts[2]

        date_data_split = date_data.split('/')
        month = int(date_data_split[0])
        day = int(date_data_split[1])
        #year = int(date_data_split[2][0:date_data_split[2].find(" ")])
        hour = int(date_data_split[2][date_data_split[2].find(" ")+1:date_data_split[2].find(":")])
        minute = int(date_data_split[2][date_data_split[2].find(":")+1:date_data_split[2].find(":")+3])
        if (date_data[len(date_data)-3:len(date_data)-1] == "PM" and hour != 12):
            hour += 12
        game_datetime = datetime(2020, month, day, hour, minute)

        teamA_name = teamA_data[1:teamA_data.rfind('(')-1]
        teamA_seed = teamA_data[teamA_data.rfind('(')+1:teamA_data.rfind(')')]
        teamA_score = teamA_data[teamA_data.rfind(')')+2:teamA_data.rfind(' ')]
        teamA = None
        if (teams != None):
            for team in teams:
                if team.name == teamA_name and team.seed == teamA_seed:
                    teamA = team

        teamB_name = teamB_data[1:teamB_data.rfind('(')-1]
        teamB_seed = teamB_data[teamB_data.rfind('(')+1:teamB_data.rfind(')')]
        teamB_score = teamB_data[teamB_data.rfind(')')+2:teamB_data.rfind(' ')]
        teamB = None
        if (teams != None):
            for team in teams:
                if team.name == teamB_name and team.seed == teamB_seed:
                    teamB = team
        
        if (teamA == None or teamB == None):
            print("error in: "  + repr(teamA_name) + " vs. " + repr(teamB_name))

        game = Game(teamA, teamB, teamA_score, teamB_score, game_datetime)
        games.append(game)
        games.sort()

    return games
    
def add_games_to_teams(teams, games):
    for game in games:
        for team in teams:
            if team.name == game.teamA.name or team.name == game.teamB.name:
                team.add_game(game)

    return teams