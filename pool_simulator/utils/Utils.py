import math;

def getPercString(value):
    return value + '%'

def getMoneyString(value):
    return '$' + value

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# returns game id for the first game in a given round. example: round 1 => 0, round 2 => 32...
def getStartinggame_idFromRound(round_num):
    return int(64 - math.pow(2, 7 - round_num))
