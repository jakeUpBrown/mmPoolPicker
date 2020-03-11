from pool_simulator.utils.DataLoader import CurrentYearPicks
from pool_simulator import PoolBuilder, BranchRunner


def run_scenario_simulation(scenario):
    # for every matchup, flip the outcome and rerun the simulations.
    # load in my picks
    picks = CurrentYearPicks.allPicks

    pool = PoolBuilder.build_pool(picks)

    num_bracket_iters = 100

    current_wins = CurrentYearPicks.year.wins
    # get all branches

    scenario_wins = scenario.get_scenario_wins(current_wins)

    # reset pool data because we want a blank pool
    pool.reset()

    BranchRunner.run_sims_with_existing_wins(pool, scenario_wins, num_bracket_iters)
    scenario.metadata = pool.get_picks_metadata()
