from pool_simulator.Branch import Branch
from pool_simulator.utils import Utils, KenPomPredictor


class Bracket:
    def __init__(self, team_list):
        self.round_num = 1
        self.teamList = team_list

    def advance_round(self, return_branches, unplayed_branches):
        # calculate the bucket size (size of number of teams that could possibly be in that position of bracket
        # in other words, round 1: bucket size 1, because there's only 1 possible team
        # round 2: bucket size 2, because it could be 1 of 2 teams, round 3: bucket size 4
        branches = list()

        starting_game_id = Utils.getStartinggame_idFromRound(self.round_num)
        bucket_size = int(pow(2, self.round_num - 1))

        num_buckets = int(len(self.teamList) / bucket_size)

        # for each bucket in the bracket, face off against the next bucket in line
        for bucketIndex in range(num_buckets):

            # if odd, skip because it's already been accounted for facing the even side
            if bucketIndex % 2 != 0:
                continue

            game_id = starting_game_id + int(bucketIndex / 2)

            b1_start_index = int(bucket_size * bucketIndex)
            b2_start_index = int(b1_start_index + bucket_size)

            is_matchup_played = False

            # face this bucket against the next bucketIndex
            # find the winner in both buckets
            bucket1_winner = None
            for b1 in range(b1_start_index, b2_start_index):
                wins = self.teamList[b1].wins
                if wins >= self.round_num:
                    bucket1_winner = self.teamList[b1]
                    is_matchup_played = True
                    break
                if wins == (self.round_num - 1):
                    bucket1_winner = self.teamList[b1]

            # only continue if not returning branches. Need to continue because played branches need to be added
            if is_matchup_played and not return_branches:
                continue

            bucket2_winner = None
            for b2 in range(b2_start_index, b2_start_index + bucket_size):
                wins = self.teamList[b2].wins
                if wins >= self.round_num:
                    bucket2_winner = self.teamList[b2]
                    is_matchup_played = True
                    break
                if wins == (self.round_num - 1):
                    bucket2_winner = self.teamList[b2]

            if is_matchup_played:
                if return_branches and not unplayed_branches:
                    branches.append(
                        Branch(bucket1_winner.team_info, bucket2_winner.team_info, self.round_num, game_id)
                    )
                continue

            if return_branches:
                if unplayed_branches:
                    branches.append(
                        Branch(bucket1_winner.team_info, bucket2_winner.team_info, self.round_num, game_id)
                    )
                continue

            bucket1_wins = KenPomPredictor.simulate_matchup(bucket1_winner.team_info, bucket2_winner.team_info, self.round_num)

            # add the pool outcome to both teams
            bucket1_winner.add_game_outcome(bucket1_wins)
            bucket2_winner.add_game_outcome(not bucket1_wins)

        self.round_num += 1

        if return_branches:
            return branches

    def load_wins(self, wins):
        i = 0
        for team in self.teamList:
            team.wins = wins[i]
            i += 1

    def get_score_from_pick_values(self, pick_values):
        score_total = 0

        for i in range(len(self.teamList)):
            score_total += pick_values[i] * self.teamList[i].wins

        return score_total

    def simulate_tourney(self):
        while self.round_num <= 6:
            self.advance_round(False, False)

    def get_win_totals(self):
        win_totals = list()

        for team in self.teamList:
            win_totals.append(team.wins)

        return win_totals

    def set_win_totals(self, win_totals):
        for i in range(len(self.teamList)):
            self.teamList[i].wins = win_totals[i]

    def print_win_totals_sorted_by_seed(self):
        team_sorted = sorted(self.teamList, key=lambda team: (team.wins, team.team_info.seed))

        for team in team_sorted:
            print(str(team.team_info.seed) + " " + team.team_info.teamName + ": " + str(team.wins))

    def reset(self):
        for team in self.teamList:
            team.reset()

        self.round_num = 1

    def get_unplayed_branches_for_current_round(self):
        self.round_num = 1
        while self.round_num <= 6:
            branches = self.advance_round(True, True)
            if len(branches) != 0:
                return branches

    def get_played_branches(self):
        self.round_num = 1
        branches = list()
        while self.round_num <= 6:
            new_branches = self.advance_round(True, False)
            # if branches is empty, return branches because we've reached a round where no matchups have been played
            if len(new_branches) == 0:
                return branches
            branches.extend(new_branches)

        return branches
