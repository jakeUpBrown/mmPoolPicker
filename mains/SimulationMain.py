import json

from pool_simulator import BranchSimulator, CurrentOddsSimulator, GamesGenerator
from pool_simulator.TeamLoader import TeamInfoContainer
from pool_simulator.Scenario import Scenario
from pool_simulator.utils import FilePathConstants
from pool_simulator.utils import Utils


def sort_meta_data_by_avg_money(meta_data_list):
    return sorted(meta_data_list, key=lambda x: (x.money_total, -1 * x.place_total), reverse=True)


TeamInfoContainer.generate_teams_json()

games_array = GamesGenerator.generate_games()

with open(FilePathConstants.get_output_file("games.json"), "w") as outfile:
    outfile.write(json.dumps(games_array, indent=2))

# CurrentOddsSimulator.run_current_year_sim()

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

scenarios = hindsight_scenarios.copy()
scenarios.extend(future_scenarios)

scenario_num = 0

users_meta_data = dict()
for scenario in scenarios:
    BranchSimulator.run_scenario_simulation(scenario)
    for meta in scenario.metadata:
        # create user list if not created
        user_meta_data = users_meta_data.setdefault(meta.user_id, [dict() for i in range(64)])
        game_obj = user_meta_data[scenario.game_id]
        game_obj.setdefault('gameId', scenario.game_id)
        teams_list = game_obj.setdefault(scenario.meta_type, [])
        meta.scenario_team_id = scenario.team_id
        teams_list.append(meta)

    print('finished scenario ' + str(scenario_num))
    scenario_num += 1

users_meta_data_json = json.loads('{}')
for (key, games_list) in users_meta_data.items():
    if key not in users_meta_data_json:
        users_meta_data_json[key] = []

    if key == '5':
        print('5 dolla holla')

    user_json = users_meta_data_json[key]
    game_id = 0
    for game in games_list:
        game_json = json.loads('{}')
        if 'GAME' in game:
            game_meta_list = game_json['GAME'] = []
            for item in sort_meta_data_by_avg_money(game['GAME']):
                j = item.get_json()
                j['teamId'] = item.scenario_team_id
                game_meta_list.append(j)
            print('game tester')
        if 'TEAM1' in game:
            team1_list = game_json['TEAM1'] = []
            for item in sort_meta_data_by_avg_money(game['TEAM1']):
                j = item.get_json()
                j['teamId'] = item.scenario_team_id
                team1_list.append(j)
            print('game tester')
        if 'TEAM2' in game:
            team2_list = game_json['TEAM2'] = []
            for item in sort_meta_data_by_avg_money(game['TEAM2']):
                j = item.get_json()
                j['teamId'] = item.scenario_team_id
                team2_list.append(j)
            print('game tester')
        user_json.append(game_json)
        game_id += 1

    print('metadata')

with open(FilePathConstants.get_output_file("gamesMetaData.json"), "w") as outfile:
    outfile.write(json.dumps(users_meta_data_json))

print('running simulation for current year')

# print('starting branch simulations for current round')
# BranchSimulator.run_current_round_branches_sim()

# print('starting bad beats simulations')
# BranchSimulator.run_bad_beats_sim()

