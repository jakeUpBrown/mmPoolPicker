import json

from pool_simulator import BranchSimulator, CurrentOddsSimulator, GamesGenerator
from pool_simulator.TeamLoader import TeamInfoContainer
from pool_simulator.Scenario import Scenario
from pool_simulator.utils import FilePathConstants
from pool_simulator.utils import Utils

TeamInfoContainer.generate_teams_json()

games_array = GamesGenerator.generate_games()

with open(FilePathConstants.get_output_file("games-list.json"), "w") as outfile:
    outfile.write(json.dumps(games_array, indent=2))

hindsight_scenarios = []
future_scenarios = []

for game in games_array:
    game_id = game['gameId']
    if game_id == 63:
        # championship game. continue
        continue

    round_num, game_offset = Utils.get_round_num_game_offset(game_id)

    if 'team1Won' in game:
        # this was a loss. Add the hindsight scenario
        losing_team_id = game['team1Id'] if game['team1Won'] is False else game['team2Id']
        scenario = Scenario(losing_team_id, round_num + 1, game_id, 'GAME')
        hindsight_scenarios.append(scenario)
        continue

    if 'team1Id' not in game and 'team2Id' not in game:
        continue

    either_team_id = game['team1Id'] if 'team1Id' in game else game['team2Id']
    # if here, we know that the game hasn't been played yet.
    # that means that both team1Id and team2Id belong to teams that have not been eliminated
    for hypothetical_win_total in range(round_num + 1, 7):
        future_game_id, meta_type = Utils.get_game_id_and_meta_type(either_team_id, hypothetical_win_total)
        if 'team1Id' in game:
            future_scenarios.append(Scenario(game['team1Id'], hypothetical_win_total, future_game_id, meta_type))
        if 'team2Id' in game:
            future_scenarios.append(Scenario(game['team2Id'], hypothetical_win_total, future_game_id, meta_type))


print('running simulation for current year')
CurrentOddsSimulator.run_current_year_sim()

# print('starting branch simulations for current round')
# BranchSimulator.run_current_round_branches_sim()

# print('starting bad beats simulations')
# BranchSimulator.run_bad_beats_sim()

