from pool_simulator.PicksMetaData import PicksMetaData
from pool_simulator.TeamValue import TeamValue


class Picks:
    def __init__(self, csv_split_values, year):
        # assuming the first element is the index, second is the name and the rest are the picks in order
        self.index = int(csv_split_values[0])
        self.name = csv_split_values[1]
        self.user_id = csv_split_values[2]
        self.year = year
        self.selected = 0

        self.pickValues = list()
        for item in csv_split_values[3:]:
            self.pickValues.append(int(item))

        self.pickDeltas = list()
        self.effectiveValues = list()
        self.points = 0
        self.place = -1
        self.metaData = None

    def set_meta_data_from_place(self, place, pool):
        if self.metaData is None:
            self.metaData = PicksMetaData(self.index, self.name, self.user_id, self.year)

        self.metaData.set_from_place(place, pool)

    def calc_points_from_win_totals(self, win_totals):
        self.points = 0
        for i in range(len(win_totals)):
            self.points += self.pickValues[i] * win_totals[i]

    def set_effective_values(self, expected_average):
        team_values = list()

        for i in range(len(self.pickValues)):
            team_values[i] = TeamValue(i, self.pickDeltas[i] + expected_average[i])

        team_values.sort(key=lambda x: x.value_assigned, reverse=True)

        current_val = 64
        for teamValue in team_values:
            teamValue.actualValue = current_val
            current_val -= 1

        team_values.sort(key=lambda x: x.team_num)

        for i in range(len(team_values)):
            self.effectiveValues[i] = team_values[i].actualValue

    def reset(self):
        self.points = 0
        self.selected += 1
