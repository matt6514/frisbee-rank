import math

def get_rating_differential(win_score, lose_score):
    r = lose_score/(win_score-1)
    rating_differential = 125 + 475*((math.sin(min(1,(1-r)/.5)*.4*math.pi))/math.sin(.4*math.pi))
    return round(rating_differential)

def get_score_weight(win_score, lose_score):
    return min(1, math.sqrt((win_score + max(lose_score, math.floor((win_score-1)/2)))/19))

#print(get_rating_differential(13, 5))
#print(get_score_weight(14, 1))
