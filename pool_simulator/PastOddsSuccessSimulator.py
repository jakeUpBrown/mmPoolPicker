import copy
import os

from pool_simulator import PoolBuilder, BranchRunner
from pool_simulator.utils.DataLoader import CurrentYearPicks, PastPicks
from pool_simulator.utils import FilePathConstants
from pool_simulator.PicksMetaData import PicksMetaData


def get_metadata_for_every_past_pick():
    # load in my picks
    picks = CurrentYearPicks.allPicks

    pool = PoolBuilder.build_pool()
    pool.picks = picks

    current_wins = CurrentYearPicks.year.wins
    num_bracket_iters = 10000

    # add dummy pick to the end of picks
    pool.picks.append(copy.copy(pool.picks[0]))

    past_odds_outfile = os.path.abspath(FilePathConstants.get_data_file("past-odds.csv"))

    with open(past_odds_outfile, "w+") as outfile:
        outfile.write(PicksMetaData.get_output_header())

    pick_num = 1

    for pastPick in PastPicks.allPicks:
        print('calculating past odds: {0}/{1}'.format(pick_num, str(len(PastPicks.allPicks))))

        pastPick.index = len(pool.picks) - 1
        pool.picks[len(pool.picks) - 1] = pastPick

        BranchRunner.run_sims_with_existing_wins(pool, current_wins, num_bracket_iters)

        with open(past_odds_outfile, "a+") as outfile:
            outfile.write(pastPick.metaData.get_file_output())

        pick_num += 1

    print('finished simulation')


get_metadata_for_every_past_pick()

