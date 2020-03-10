import os

from pool_simulator.utils.DataLoader import CurrentYearPicks
from pool_simulator import PoolBuilder, BranchRunner
from pool_simulator.utils import FilePathConstants


def run_current_round_branches_sim():
    # load in my picks
    picks = CurrentYearPicks.allPicks

    pool = PoolBuilder.build_pool()
    pool.picks = picks

    num_bracket_iters = 150

    current_wins = CurrentYearPicks.year.wins
    # get all branches
    pool.load_wins(current_wins)

    branches = pool.bracket.get_unplayed_branches_for_current_round()
    if branches is None:
        print('no more games to be played')
        return

    # delete the branch odds file
    branch_out_file = os.path.abspath(FilePathConstants.get_output_file("branch-odds.csv"))
    if os.path.exists(branch_out_file):
        os.remove(branch_out_file)

    # reset pool data because we want a blank pool
    pool.reset()

    branch_num = 1

    for branch in branches:
        print("Running " + str(branch_num) + "/" + str(len(branches)) +
              " simulation for " + branch.team1_name + " vs " + branch.team2_name)
        # change wins for the branch team 1
        new_wins = current_wins.copy()
        new_wins[branch.team1_index] += 1

        # run simulation
        BranchRunner.run_sims_with_existing_wins(pool, new_wins, num_bracket_iters)

        # save metadata
        branch.team1_win_meta_data = pool.get_picks_metadata()

        # change wins for the branch team 2
        new_wins[branch.team1_index] -= 1
        new_wins[branch.team2_index] += 1

        print(branch.team1_name)
        # pool.print_bet_data()
        pool.reset_bet_data()

        # run simulation
        BranchRunner.run_sims_with_existing_wins(pool, new_wins, num_bracket_iters)

        # save metadata
        branch.team2_win_meta_data = pool.get_picks_metadata()

        branch.append_meta_data_to_file(branch_out_file)

        print(branch.team2_name)
        # pool.print_bet_data()
        pool.reset_bet_data()

        branch_num += 1

    print('finished simulation')


def run_bad_beats_sim():
    # for every matchup, flip the outcome and rerun the simulations.
    # load in my picks
    picks = CurrentYearPicks.allPicks

    pool = PoolBuilder.build_pool()
    pool.picks = picks

    num_bracket_iters = 100

    current_wins = CurrentYearPicks.year.wins
    # get all branches
    pool.load_wins(current_wins)

    branches = pool.bracket.get_played_branches()

    # delete the branch odds file
    branch_out_file = os.path.abspath(FilePathConstants.get_output_file("bad-beats.csv"))
    if os.path.exists(branch_out_file):
        os.remove(branch_out_file)

    # reset pool data because we want a blank pool
    pool.reset()

    branch_num = 1

    for branch in branches:
        print("Running " + str(branch_num) + "/" + str(len(branches)) +
              " simulation for " + branch.team1_name + " vs " + branch.team2_name)
        # change wins for the branch team 1
        team1_won = current_wins[branch.team1_index] > current_wins[branch.team2_index]

        new_wins = current_wins.copy()
        new_wins[branch.team1_index if team1_won else branch.team2_index] = branch.round_num
        new_wins[branch.team2_index if team1_won else branch.team1_index] += 1

        # run simulation
        BranchRunner.run_sims_with_existing_wins(pool, new_wins, num_bracket_iters)

        # save metadata
        if team1_won:
            branch.team2_win_meta_data = pool.get_picks_metadata()
        else:
            branch.team1_win_meta_data = pool.get_picks_metadata()

        branch.append_meta_data_as_bad_beat(branch_out_file)

        # metaData = branch.getRelevantMetaData()
        # badBeatsJson = metaData.get_bad_beats_json()

        branch_num += 1

    print('finished simulation')