import json


class PicksMetaData:
    def __init__(self, index, name, user_id, year):
        self.index = index
        self.name = name
        self.user_id = user_id
        self.year = year
        self.sampleSize = 0
        self.first_count = 0
        self.second_count = 0
        self.last_count = 0
        self.place_total = 0
        self.money_total = 0
        self.scenario_team_id = -1

    @classmethod
    def from_csv(cls, items):
        instance = cls(int(items[0]), items[1], int(items[2]), int(items[3]))
        count = 10000
        instance.sampleSize = count
        instance.money_total = int(float(items[4][1:]) * count)
        instance.first_count = int(float(items[5][:(len(items[5]) - 1)]) * count)
        instance.second_count = int(float(items[6][:(len(items[6]) - 1)]) * count)
        instance.last_count = int(float(items[7][:(len(items[7]) - 1)]) * count)
        instance.place_total = int(float(items[8]) * count)

        return instance

    def reset_stats(self):
        self.sampleSize = 0
        self.first_count = 0
        self.second_count = 0
        self.last_count = 0
        self.place_total = 0
        self.money_total = 0

    def set_from_place(self, place, pool):
        self.sampleSize += 1
        self.first_count += pool.get_first_win_share(place)
        self.second_count += pool.get_second_win_share(place)
        self.last_count += pool.get_last_win_share(place)
        self.money_total += pool.get_money_total_from_place(place)
        self.place_total += place

    def round_value(self, value):
        return str(round((value * 100) / self.sampleSize, 2))

    def get_first_perc(self):
        return self.round_value(self.first_count)

    def get_second_perc(self):
        return self.round_value(self.second_count)

    def get_last_perc(self):
        return self.round_value(self.last_count)

    def get_avg_money(self):
        return round(self.money_total / self.sampleSize, 2)

    def get_avg_place(self):
        return round(self.place_total / self.sampleSize, 2)

    def print(self):
        print(str(self.index) + ": " + self.name + " - " + str(self.year))
        print("simulated " + str(self.sampleSize) + " iterations")
        print("first: " + str(self.get_first_perc()) + '%')
        print("second: " + str(self.get_second_perc()) + '%')
        print("dead last: " + str(self.get_last_perc()) + '%')
        print("average place: " + str(self.get_avg_place()))
        print("average money: $" + str(self.get_avg_money()))

    def print_line(self):
        print(str(self.index) +
              ": " + self.name +
              "," + self.user_id +
              " - " + str(self.year) +
              ", $" + str(self.get_avg_money()) +
              ", first: " + str(self.get_first_perc()) + '%'
              ", second: " + str(self.get_second_perc()) + '%'
              ", deadLast: " + str(self.get_last_perc()) + '%'
              ", averagePlace: " + str(self.get_avg_place()) + "\n")

    def get_file_output(self):
        return (str(self.index) +
                "," + self.name +
                "," + self.user_id +
                "," + str(self.year) +
                ",$" + str(self.get_avg_money()) +
                "," + str(self.get_first_perc()) + '%'
                "," + str(self.get_second_perc()) + '%'
                "," + str(self.get_last_perc()) + '%'
                "," + str(self.get_avg_place()) + "\n")

    def get_bad_beat_file_output(self, team_id, num_wins, game_id):
        return (self.name +
                "," + self.user_id +
                "," + str(team_id) +
                "," + str(num_wins) +
                "," + str(game_id) +
                ",$" + str(self.get_avg_money()) +
                "," + str(self.get_first_perc()) + '%'
                "," + str(self.get_second_perc()) + '%'
                "," + str(self.get_last_perc()) + '%'
                "," + str(self.get_avg_place())
                + "\n")

    def get_json(self):
        player_json = json.loads('{}')
        player_json['avgMoney'] = self.get_avg_money()
        player_json['perc1st'] = self.get_first_perc()
        player_json['perc2nd'] = self.get_second_perc()
        player_json['percLast'] = self.get_last_perc()
        player_json['avgPlace'] = self.get_avg_place()
        player_json['userId'] = self.user_id

        return player_json

    def get_current_odds_json(self):
        current_odds_json = self.get_json()
        return current_odds_json

    def get_bad_beats_json(self):
        bad_beats_json = self.get_json()
        return bad_beats_json

    @staticmethod
    def get_output_header():
        return "index,name,user_id,year,avg money,first%,second%,last%,avg place\n"

    @staticmethod
    def get_bad_beats_row_header():
        return "name,user_id,team_id,num_wins,game_id,avg money,first%,second%,last%,avg place\n"

    def subtract_other_metadata(self, meta_data):
        self.first_count -= meta_data.first_count
        self.second_count -= meta_data.second_count
        self.last_count -= meta_data.last_count
        self.money_total -= meta_data.money_total
        self.place_total -= meta_data.place_total
