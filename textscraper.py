from datetime import datetime
from classes import Team, Game

lines = None
with open ('games.txt') as games:
    lines = games.readlines()

for line in lines:
    line = line.strip()
    parts = line.split('|')
    date = parts[0]
    print(parts)
