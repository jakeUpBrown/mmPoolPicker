import math
import random


def getTeam1WinProb(adj_em1, adj_t1, adj_em2, adj_t2, round_num):
    # KenPom uses 11 points for the standard deviation. I want to increase that as the rounds progress
    # the reasoning for this sigma growth is that the matchups should move closer to a coin-flip as teams advance.
    sigma_growth_coeff = 1
    sigma = 11 + (sigma_growth_coeff * round_num)

    proj_spread = (adj_em1 - adj_em2) * (adj_t1 + adj_t2) / 200
    win_prob = 1 - (.5 * (1 + math.erf((0 - proj_spread) / (sigma*math.sqrt(2)))))
    return win_prob


def get_random_outcome(win_prob):
    # winProb is float value out of 100
    # multiple by 100 and convert to int
    # generate number between 0 and (100 * 100)
    # if randomNumber is less than winProb, return True, else False
    perc_decimals = 2
    multiply_factor = pow(10, 2 + perc_decimals)
    return random.randrange(1 * multiply_factor) < (win_prob * multiply_factor)


# simulate the matchup and return boolean of whether team 1 won
def simulate_matchup(team1_info, team2_info, round_num):
    winProb = getTeam1WinProb(team1_info.adj_em, team1_info.adj_t, team2_info.adj_em, team2_info.adj_t, round_num)

    return get_random_outcome(winProb)

