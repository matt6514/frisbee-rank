from classes import Team, Game
from webscraper import get_tournament
from algorithm import *

url = "https://play.usaultimate.org/events/USA-Ultimate-College-Championships-2021/schedule/Men/CollegeMen/d_i_men/"
#url = "https://play.usaultimate.org/events/2017-US-Open-Club-Championships/schedule/Boys/youth-club-u-20-boys/"

tournament = get_tournament(url)
name = tournament['name']
teams = tournament['teams']
games = tournament['games']

for i in range(0, 100):
    for game in games:
        if game.teamA_score[0].isdigit():
            rating_diff = get_rating_differential(int(game.teamA_score), int(game.teamB_score))
            if (game.teamA.rating > game.teamB.rating + 600 and int(game.teamA_score) > int(game.teamB_score) * 2 + 1):
                continue
            elif (game.teamB.rating > game.teamA.rating + 600 and int(game.teamB_score) > int(game.teamA_score) * 2 + 1):
                continue
            if (int(game.teamA_score) > int(game.teamB_score)):
                game.teamA.game_ratings.append((game.teamA.rating + rating_diff) * get_score_weight(int(game.teamA_score), int(game.teamB_score)))
                game.teamB.game_ratings.append((game.teamB.rating - rating_diff) * get_score_weight(int(game.teamB_score), int(game.teamA_score)))
            else:
                game.teamA.game_ratings.append((game.teamA.rating - rating_diff) * get_score_weight(int(game.teamA_score), int(game.teamB_score)))
                game.teamB.game_ratings.append((game.teamB.rating + rating_diff) * get_score_weight(int(game.teamB_score), int(game.teamA_score)))

    for team in teams:
        if len(team.game_ratings) > 0:
            team.rating = sum(team.game_ratings)/len(team.game_ratings)

for team in teams:
    print(team.name + " " + str(round(team.rating)))
