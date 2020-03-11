import json

from pool_simulator.utils import Utils
from pool_simulator.utils.DataLoader import CurrentYearPicks


def generate_games():
    current_wins = CurrentYearPicks.year.wins

    games_array = []

    # for games 0 - 62, find the first and last bucket_index
    for game_id in range(0, 64):
        game = json.loads('{}')
        game['gameId'] = game_id
        round_num, game_offset = Utils.get_round_num_game_offset(game_id)
        t1_bucket_st, t2_bucket_st, bucket_size = Utils.get_bucket_indices_by_game_id(game_id)

        team1_index = Utils.get_winning_team_index(t1_bucket_st, bucket_size, current_wins, round_num)
        if team1_index is not None:
            game['team1Id'] = team1_index
            if current_wins[team1_index] > round_num:
                game['team1Won'] = True

        team2_index = Utils.get_winning_team_index(t2_bucket_st, bucket_size, current_wins, round_num)
        if team2_index is not None:
            game['team2Id'] = team2_index
            if current_wins[team2_index] > round_num:
                game['team1Won'] = False

        games_array.append(game)

    return games_array
