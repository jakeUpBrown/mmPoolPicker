from pool_simulator.PicksMetaData import PicksMetaData
from pool_simulator.utils import Utils


class Scenario:
    def __init__(self, team_id, num_wins, game_id, meta_type):
        self.team_id = team_id
        self.num_wins = num_wins
        self.game_id = game_id
        self.meta_type = meta_type
        self.metadata = None

    def append_meta_data_to_file(self, filename):
        with open(filename, "a+") as outfile:
            outfile.write('team-id: ' + self.team_id + ', win=' + self.num_wins + "\n")
            outfile.write(PicksMetaData.get_output_header())

            for metaData in sorted(self.metadata, key=lambda pick: pick.money_total, reverse=True):
                outfile.write(metaData.get_file_output())

            outfile.write("\n")

    def append_meta_data_as_bad_beat(self, filename):
        with open(filename, "a+") as outfile:

            outfile.write(PicksMetaData.get_bad_beats_row_header())
            for metaData in sorted(self.metadata, key=lambda pick: pick.money_total, reverse=True):
                outfile.write(metaData.get_bad_beat_file_output(self.team_id, self.num_wins, self.game_id))

            outfile.write("\n")

    def get_scenario_wins(self, current_wins):
        # number of wins is the round that is attempting to be redone
        # in that case, find the
        new_wins = current_wins.copy()

        t1_bucket_st, t2_bucket_st, bucket_size = Utils.get_bucket_indices_by_game_id(self.game_id)

        # if the t2_bucket_st is None then it should be assumed to look in the first bucket, because that will include every team
        if t2_bucket_st is not None and self.team_id < t2_bucket_st:
            # need to find the other team in t2_bucket
            bucket_st = t2_bucket_st
        else:
            # need to find the other team in t1_bucket
            bucket_st = t1_bucket_st

        winning_team_index = Utils.get_winning_team_index(bucket_st, bucket_size, current_wins, self.num_wins)
        if winning_team_index is not None:
            new_wins[winning_team_index] = self.num_wins - 1

        new_wins[self.team_id] = self.num_wins
        return new_wins
