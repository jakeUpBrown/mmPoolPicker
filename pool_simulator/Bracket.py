from pool_simulator.utils import Utils, KenPomPredictor


class Bracket:
    def __init__(self, team_list):
        self.round_num = 0
        self.team_list = team_list

    def advance_round(self):
        # calculate the bucket size (size of number of teams that could possibly be in that position of bracket
        # in other words, round 0: bucket size 1, because there's only 1 possible team
        # round 0: bucket size 1 round 1: bs 2,, round 2: bs 4
        bucket_size = Utils.get_bucket_size_by_round_num(self.round_num)

        num_buckets = int(len(self.team_list) / bucket_size)

        # for each bucket in the bracket, face off against the next bucket in line
        for bucketIndex in range(num_buckets):

            # if odd, skip because it's already been accounted for facing the even side
            if bucketIndex % 2 != 0:
                continue

            b1_start_index = int(bucket_size * bucketIndex)
            b2_start_index = int(b1_start_index + bucket_size)

            is_matchup_played = False

            # face this bucket against the next bucketIndex
            # find the winner in both buckets
            bucket1_winner = None
            for b1 in range(b1_start_index, b2_start_index):
                wins = self.team_list[b1].wins
                if wins > self.round_num:
                    bucket1_winner = self.team_list[b1]
                    is_matchup_played = True
                    break
                if wins == self.round_num:
                    bucket1_winner = self.team_list[b1]

            # only continue if not returning branches. Need to continue because played branches need to be added
            if is_matchup_played:
                continue

            bucket2_winner = None
            for b2 in range(b2_start_index, b2_start_index + bucket_size):
                wins = self.team_list[b2].wins
                if wins > self.round_num:
                    bucket2_winner = self.team_list[b2]
                    is_matchup_played = True
                    break
                if wins == self.round_num:
                    bucket2_winner = self.team_list[b2]

            if is_matchup_played:
                continue

            bucket1_wins = KenPomPredictor.simulate_matchup(bucket1_winner.team_info, bucket2_winner.team_info,
                                                            self.round_num)

            # add the game outcome to both teams
            bucket1_winner.add_game_outcome(bucket1_wins)
            bucket2_winner.add_game_outcome(not bucket1_wins)

        self.round_num += 1

    def load_wins(self, wins):
        i = 0
        for team in self.team_list:
            team.wins = wins[i]
            i += 1

    def get_score_from_pick_values(self, pick_values):
        score_total = 0

        for i in range(len(self.team_list)):
            score_total += pick_values[i] * self.team_list[i].wins

        return score_total

    def simulate_tourney(self):
        while self.round_num < 6:
            self.advance_round()

    def get_win_totals(self):
        win_totals = list()

        for team in self.team_list:
            win_totals.append(team.wins)

        return win_totals

    def set_win_totals(self, win_totals):
        for i in range(len(self.team_list)):
            self.team_list[i].wins = win_totals[i]

    def print_win_totals_sorted_by_seed(self):
        team_sorted = sorted(self.team_list, key=lambda team: (team.wins, team.team_info.seed))

        for team in team_sorted:
            print(str(team.team_info.seed) + " " + team.team_info.teamName + ": " + str(team.wins))

    def reset(self):
        for team in self.team_list:
            team.reset()

        self.round_num = 0


