from classes import Team, Game
from webscraper import get_tournament
from textscraper import get_games, add_games_to_teams
from algorithm import get_rating_differential, get_score_weight

# urls = []
#     "https://play.usaultimate.org/events/USA-Ultimate-College-Championships-2021/schedule/Men/CollegeMen/d_i_men/",
#     "https://play.usaultimate.org/events/Atlantic-Coast-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/",
#     "https://play.usaultimate.org/events/Great-Lakes-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/",
#     "https://play.usaultimate.org/events/Metro-East-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/",
#     "https://play.usaultimate.org/events/Northwest-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/",
#     "https://play.usaultimate.org/events/New-England-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/",
#     "https://play.usaultimate.org/events/North-Central-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/",
#     "https://play.usaultimate.org/events/Ohio-Valley-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/",
#     "https://play.usaultimate.org/events/South-Central-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/",
#     "https://play.usaultimate.org/events/Southwest-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/",
#     "https://play.usaultimate.org/events/Southeast-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/"
# ]
urls = [
    "https://play.usaultimate.org/events/USA-Ultimate-College-Championships-2021/schedule/Women/CollegeWomen/d_i_women/",
    "https://play.usaultimate.org/events/Atlantic-Coast-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/",
    "https://play.usaultimate.org/events/Great-Lakes-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/",
    "https://play.usaultimate.org/events/Metro-East-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/",
    "https://play.usaultimate.org/events/Northwest-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/",
    "https://play.usaultimate.org/events/New-England-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/",
    "https://play.usaultimate.org/events/North-Central-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/",
    "https://play.usaultimate.org/events/Ohio-Valley-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/",
    "https://play.usaultimate.org/events/South-Central-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/",
    "https://play.usaultimate.org/events/Southwest-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/",
    "https://play.usaultimate.org/events/Southeast-D-I-College-Womens-Regionals-2021/schedule/Women/CollegeWomen/"
]
tournaments = []
games = []
teams = []

for url in urls:
    print(url)
    tournaments.append(get_tournament(url))

for tournament in tournaments:
    for t_game in tournament.games:
        games.append(t_game)
    for team in tournament.teams:
        if team not in teams:
            teams.append(team)

#runs usau algorithm n times
#usually converges within a few thousand
n = 2000
for i in range(0, n):
    for game in games:
        if game.teamA_score[0].isdigit():
            if (game.teamA.rating > game.teamB.rating + 600 and int(game.teamA_score) > int(game.teamB_score) * 2 + 1):
                #print("blowout " + game.teamA.name + " vs. " + game.teamB.name)
                continue
            elif (game.teamB.rating > game.teamA.rating + 600 and int(game.teamB_score) > int(game.teamA_score) * 2 + 1):
                #print("blowout " + game.teamA.name + " vs. " + game.teamB.name)
                continue
            if (int(game.teamA_score) > int(game.teamB_score)):
                rating_diff = get_rating_differential(int(game.teamA_score), int(game.teamB_score))
                game.teamA.game_ratings.append((game.teamB.rating + rating_diff) * get_score_weight(int(game.teamA_score), int(game.teamB_score)))
                game.teamB.game_ratings.append((game.teamA.rating - rating_diff) * get_score_weight(int(game.teamA_score), int(game.teamB_score)))
            else:
                rating_diff = get_rating_differential(int(game.teamB_score), int(game.teamA_score))
                game.teamA.game_ratings.append((game.teamB.rating - rating_diff) * get_score_weight(int(game.teamB_score), int(game.teamA_score)))
                game.teamB.game_ratings.append((game.teamA.rating + rating_diff) * get_score_weight(int(game.teamB_score), int(game.teamA_score)))

    for team in teams:
        if len(team.game_ratings) > 0:
            # if (team.name == "North Carolina"):
            #     print(team.game_ratings)
            team.rating = sum(team.game_ratings)/len(team.game_ratings)
            team.game_ratings = []

teams.sort()
i = 1
for team in teams:
    print(str(i) + ". " + team.name + " " + str(round(team.rating)))
    i += 1