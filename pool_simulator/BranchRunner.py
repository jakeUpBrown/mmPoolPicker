def run_sims_with_existing_wins(pool, wins, num_bracket_iters):
    # load in my picks
    pool.reset_picks_metadata()

    # for y -> 100, generate random bracket outcomes and check how likely we are to win
    for y in range(num_bracket_iters):
        # create a new pool using myPicks, otherPicks, and the bracket
        pool.load_wins(wins)
        pool.run_full_sim()
