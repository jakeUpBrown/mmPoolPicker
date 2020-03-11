from pool_simulator import PoolBuilder
from pool_simulator.utils.DataLoader import PastPicks
from pool_simulator.utils import FilePathConstants
from pool_simulator.PicksMetaData import PicksMetaData


def get_metadata_for_pick_index(index):
    print("loading picks at index " + str(index))
    # load in my picks
    my_picks = PastPicks.load_picks_by_index(index)

    num_wins = 0.0
    num_seconds = 0.0
    num_dead_lasts = 0.0

    total_place = 0.0
    total_money = 0.0

    num_random_set_iters = 200
    num_bracket_iters = 200

    pool = PoolBuilder.build_pool(my_picks)

    # for x -> number of specified random set iterations, generate random set of opponent picks
    for x in range(num_random_set_iters):
        other_picks = PastPicks.get_random_other_picks_set(index)

        print('pick indices:')
        for otherPick in other_picks:
            print(otherPick.index)

        pool.setOtherPicks(other_picks)

        # for y -> 100, generate random bracket outcomes and check how likely we are to win
        for y in range(num_bracket_iters):
            # create a new pool instance using my_picks, other_picks, and the bracket
            pool.simulate_tourney()
            place = pool.getMyPlace()

            pool.bracket.print_win_totals_sorted_by_seed()

            shared_count = (place - int(place)) * 10
            win_value = 1 / (1 + shared_count)

            if place < 2:
                num_wins += win_value
            elif place < 3:
                num_seconds += win_value
            elif place >= pool.get_last_place():
                num_dead_lasts += win_value

            total_place += place
            total_money += pool.get_money_total_from_place(place)

            pool.reset()

    num_simulations = num_random_set_iters * num_bracket_iters

    picks_meta_data = PicksMetaData()
    picks_meta_data.picks = my_picks
    picks_meta_data.sampleSize = num_simulations
    picks_meta_data.firstPerc = num_wins * 100 / num_simulations
    picks_meta_data.secondPerc = num_seconds * 100 / num_simulations
    picks_meta_data.deadLastPerc = num_dead_lasts * 100 / num_simulations
    picks_meta_data.averagePlace = total_place / num_simulations
    picks_meta_data.averageMoney = total_money / num_simulations

    picks_meta_data.print_line()

    return picks_meta_data
    # get average payout from all simulations


def calc_all_picks_metadata():

    picks_meta_data_list = list()
    for pickIndex in range(len(PastPicks.allPicks)):
        picks_meta_data_list.append(get_metadata_for_pick_index(pickIndex))

    picks_meta_data_list.sort(key=lambda pick: pick.averageMoney, reverse=True)

    print("\n\npick distribution:")
    for pick in PastPicks.allPicks:
        print(pick.selected)

    print("\n\n\nFINAL SORTED PICKS META DATA\n\n\n")

    with open(FilePathConstants.get_output_file("picks-metadata.csv"), "w") as outfile:
        for picksMetaData in picks_meta_data_list:
            outfile.write(picksMetaData.get_file_output())


PastPicks.calc_effective_values()
calc_all_picks_metadata()
