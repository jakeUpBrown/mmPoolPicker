from pool_simulator.PicksMetaData import PicksMetaData


class Branch:
    def __init__(self, team1, team2, round_num, game_id):
        self.team1_index = team1.team_num
        self.team1_name = team1.team_name
        self.team2_index = team2.team_num
        self.team2_name = team2.team_name
        self.round_num = round_num
        self.game_id = game_id
        self.team1_win_meta_data = None
        self.team2_win_meta_data = None

    def append_meta_data_to_file(self, filename):
        with open(filename, "a+") as outfile:

            if self.team1_win_meta_data is not None:

                outfile.write('Winner: ' + self.team1_name + '-' + str(self.team1_index) + ', Loser: ' +
                              self.team2_name + '-' + str(self.team2_index) + "\n")
                outfile.write(PicksMetaData.get_output_header())

                for metaData in sorted(self.team1_win_meta_data, key=lambda pick: pick.money_total, reverse=True):
                    outfile.write(metaData.get_file_output())

                outfile.write("\n")

            if self.team2_win_meta_data is not None:

                outfile.write('Winner: ' + self.team2_name + '-' + str(self.team2_index) + ', Loser: ' +
                              self.team1_name + '-' + str(self.team1_index) + "\n")

                outfile.write(PicksMetaData.get_output_header())

                for metaData in sorted(self.team2_win_meta_data, key=lambda pick: pick.money_total, reverse=True):
                    outfile.write(metaData.get_file_output())

                outfile.write("\n")

    def append_meta_data_as_bad_beat(self, filename):
        with open(filename, "a+") as outfile:

            outfile.write(PicksMetaData.get_bad_beats_row_header())

            if self.team1_win_meta_data is not None:
                for metaData in sorted(self.team1_win_meta_data, key=lambda pick: pick.money_total, reverse=True):
                    outfile.write(metaData.get_bad_beat_file_output(self.team2_name, self.team1_name, self.game_id))
            else:
                for metaData in sorted(self.team2_win_meta_data, key=lambda pick: pick.money_total, reverse=True):
                    outfile.write(metaData.get_bad_beat_file_output(self.team1_name, self.team2_name, self.game_id))

            outfile.write("\n")

    def get_relevant_meta_data(self):
        if self.team1_win_meta_data is not None:
            return self.team1_win_meta_data

        if self.team2_win_meta_data is not None:
            return self.team2_win_meta_data

        return None
