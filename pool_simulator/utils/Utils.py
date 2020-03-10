import math


def get_perc_string(value):
    return value + '%'


def get_money_string(value):
    return '$' + value


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# returns game id for the first game in a given round. example: round 0 => 0, round 1 => 32...
def get_starting_game_id_from_round(round_num):
    return int(64 - math.pow(2, 6 - round_num))


def get_bucket_size_by_round_num(round_num):
    return int(pow(2, round_num))


def get_round_num_game_offset(game_id):
    starting_id_in_round = 0
    for i in range(0, 6):
        starting_game_id_in_next_round = get_starting_game_id_from_round(i + 1)
        if game_id < starting_game_id_in_next_round:
            game_offset = game_id - starting_id_in_round
            return i, game_offset
        else:
            starting_id_in_round = starting_game_id_in_next_round

    return 6, 0


def get_bucket_indices_by_game_id(game_id):
    round_num, game_offset = get_round_num_game_offset(game_id)
    bucket_size = get_bucket_size_by_round_num(round_num)

    t1_bucket_st = (game_offset * bucket_size * 2)
    t2_bucket_st = None
    if round_num != 6:
        t2_bucket_st = t1_bucket_st + bucket_size

    return t1_bucket_st, t2_bucket_st, bucket_size


def get_winning_team_index(start_index, bucket_size, current_wins, round_num):
    if start_index is None:
        return None

    for t_index in range(start_index, start_index + bucket_size):
        if current_wins[t_index] >= round_num:
            return t_index

    return None


def get_game_id_and_meta_type(team_id, round_num):
    bucket_size = get_bucket_size_by_round_num(round_num)
    starting_game_id_for_round = get_starting_game_id_from_round(round_num)
    # if the team_id is in the lower bucket, it will be team 1
    meta_type = 'TEAM1' if ((team_id % (bucket_size * 2)) < bucket_size) else 'TEAM2'

    # since there are 2 buckets per game...
    # the int return of either team id divided by double bucket size will tell you the game_id offset for the round
    future_game_id = starting_game_id_for_round + int(team_id / (bucket_size * 2))

    return future_game_id, meta_type

