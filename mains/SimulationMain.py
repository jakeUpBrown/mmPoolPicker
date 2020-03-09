from pool_simulator import BranchSimulator, CurrentOddsSimulator

print('running simulation for current year')
CurrentOddsSimulator.run_current_year_sim()

print('starting branch simulations for current round')
BranchSimulator.run_current_round_branches_sim()

print('starting bad beats simulations')
BranchSimulator.run_bad_beats_sim()

