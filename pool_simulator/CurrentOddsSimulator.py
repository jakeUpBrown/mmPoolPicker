import os

from pool_simulator.utils.DataLoader import CurrentYearPicks

# create bracket using picks

# set which picks we want to be ours

# set other picks

# load in wins
from pool_simulator import PoolBuilder, BranchRunner
from pool_simulator.utils.FilePathConstants import FilePathConstants


def run_current_year_sim():
    # load in my picks
    picks = CurrentYearPicks.allPicks

    pool = PoolBuilder.build_pool()
    pool.picks = picks

    num_bracket_iters = 500

    current_wins = CurrentYearPicks.year.wins

    BranchRunner.run_sims_with_existing_wins(pool, current_wins, num_bracket_iters)

    pool.print_metadata_to_file(os.path.abspath(FilePathConstants.get_output_file("current-odds.csv")))
    pool.print_meta_data_to_json(os.path.abspath(FilePathConstants.get_output_file("current-odds.json")))
    # pool.print_bet_data()

    print('finished simulation')

