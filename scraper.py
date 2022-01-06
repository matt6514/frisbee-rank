from bs4 import BeautifulSoup
import requests
from datetime import datetime
from classes import Team, Game

page = requests.get("https://play.usaultimate.org/events/USA-Ultimate-College-Championships-2021/schedule/Men/CollegeMen/d_i_men/")
#page = requests.get("https://play.usaultimate.org/events/2017-US-Open-Club-Championships/schedule/Boys/youth-club-u-20-boys/")

soup = BeautifulSoup(page.content, 'html.parser')
tournament_name = soup.find("div", {"class": "breadcrumbs"}).find_all("a")[1].contents[0]

num_pools = len(soup.find_all("div", {"class": "clearfix"})[1].find_all("div", {"class": "pool"}))

pools = soup.find_all("div", {"class": "pool"})[0:num_pools]
pools_games = soup.find_all("table", {"class": "global_table scores_table"})
teams = []
games = []

#creates list of teams from pools
for pool in pools:
    pool_letter = pool.find("h3").contents[0][5]
    for row in pool.find("table").find("tbody").find_all("a"):
        name = row.contents[0][0:row.contents[0].find('(')-1]
        seed = row.contents[0][row.contents[0].rfind('(')+1:row.contents[0].rfind(')')]
        teams.append(Team(name, seed, pool_letter))

teams.sort()

#scrapes pools games
for pool in pools_games:
    pool_letter = pool.find("th").contents[0][5]
    for row in pool.find("tbody").find_all("tr"):
        if row.has_attr("data-game"):
            teamA_name = row.find_all("td")[3].find("a").contents[0]
            teamB_name = row.find_all("td")[4].find("a").contents[0]
            teamA, teamB = None, None
            for team in teams:
                if team.name in teamA_name:
                    teamA = team
                elif team.name in teamB_name:
                    teamB = team
            teamA_score = row.find_all("td")[5].find_all("span", {"class": "isScore"})[0].find("span").contents[0]
            teamB_score = row.find_all("td")[5].find_all("span", {"class": "isScore"})[1].find("span").contents[0]

            date = row.find_all("td")[0].find("span").contents[0]
            time = row.find_all("td")[1].find("span").contents[0]
            month = int(date[4:date.find('/')])
            day = int(date[date.find('/')+1:len(date)])
            hour = int(time[0:time.find(":")])
            minute = int(time[time.find(":")+1:time.find(":")+3])
            if (time[len(time)-2:len(time)] == "PM" and hour != 12):
                hour += 12
            game_datetime = datetime(2020, month, day, hour, minute)

            game = Game(teamA, teamB, teamA_score, teamB_score, game_datetime, pool_letter)
            games.append(game)
            teamA.add_game(game)
            teamB.add_game(game)

games.sort()

# for team in teams:
#     team.print_team()

for game in games:
    game.print_game()
