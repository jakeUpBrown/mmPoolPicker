import json

from pool_simulator.utils.DataLoader import CurrentYearPicks
from pool_simulator.PicksMetaData import PicksMetaData
import copy


class Pool:
    def __init__(self, bracket):
        self.bracket = bracket
        self.picks = None
        self.buy_in = 20
        self.jake_wins = 0
        self.dad_wins = 0
        self.ties = 0
        self.overall_ties = 0

    def sim_tourney(self):
        self.bracket.simulate_tourney()

    def run_full_sim(self):
        self.sim_tourney()
        self.set_picks_metadata()
        self.reset()

    def calc_point_totals(self):
        for pick in self.picks:
            pick.calc_points_from_win_totals(self.bracket.get_win_totals())

    def get_place_at_pick_index(self, pick_index):
        self.calc_point_totals()

        place = 1.0

        current_pick = self.picks[pick_index]

        for pick in self.picks:
            if pick.index == current_pick.index:
                continue

            if pick.points > current_pick.points:
                place += 1
            elif pick.points == current_pick.points:
                place += .1

        return place

    def get_money_total_from_place(self, place):
        total_money_amount = self.buy_in * (len(self.picks))

        loser_amount = (self.buy_in / 2)
        winner_cut = .8

        perc_of_cut = Pool.get_perc_of_cut(place)

        if place >= self.get_last_place():
            return loser_amount * perc_of_cut

        total_money_amount -= loser_amount

        if place < 2:
            return (total_money_amount * winner_cut) * perc_of_cut

        total_money_amount -= (total_money_amount * winner_cut)

        if place < 3:
            return total_money_amount * perc_of_cut

        return 0

    def get_first_win_share(self, place):
        return Pool.get_win_share_by_target(place, 1)

    def get_second_win_share(self, place):
        return Pool.get_win_share_by_target(place, 2)

    def get_last_win_share(self, place):
        return Pool.get_win_share_by_target(place, self.get_last_place())

    @classmethod
    def get_win_share_by_target(cls, place, target_place):
        if target_place <= place < (target_place + 1):
            return Pool.get_perc_of_cut(place)

        return 0
    
    @staticmethod
    def get_perc_of_cut(place):
        return 1 / (1 + ((place - int(place)) * 10))
    
    def get_last_place(self):
        return len(self.picks)

    def reset(self):
        for pick in self.picks:
            pick.reset()
        self.bracket.reset()

    def load_wins(self, wins):
        self.bracket.load_wins(wins)

    def set_picks_metadata(self):
        self.calc_point_totals()
        sorted_picks = sorted(self.picks, key=lambda x: x.points, reverse=True)

        last_point_total = sorted_picks[0].points
        last_index_set = -1
        win_share = 0

        for i in range(1, len(sorted_picks) + 1):
            if i < len(sorted_picks) and sorted_picks[i].points == last_point_total:
                win_share += 0.1
            else:
                # set place until last_index_set
                indexToSet = i - 1
                placeToSet = last_index_set + 2 + win_share
                while indexToSet > last_index_set:
                    sorted_picks[indexToSet].place = placeToSet
                    indexToSet -= 1

                last_index_set = i - 1
                last_point_total = sorted_picks[i].points if (i < len(sorted_picks)) else 0
                win_share = 0

        # now sorted picks should hold the correct places
        # go through and set the picks metadata at the appropriate index
        for sortedPick in sorted_picks:
            self.picks[sortedPick.index].set_meta_data_from_place(sortedPick.place, self)

        jake_place = self.picks[13].place
        dad_place = self.picks[1].place

        self.jake_wins += 1 if (jake_place < dad_place) else 0
        self.ties += 1 if (jake_place == dad_place) else 0
        self.dad_wins += 1 if (jake_place > dad_place) else 0

        if sorted_picks[0].place > 1:
            self.overall_ties += 1

    def print_bet_data(self):
        total = self.jake_wins + self.dad_wins + self.ties
        print("dad win percentage: " + str(round((self.dad_wins * 100 / total), 2)) + "%")
        print("jake win percentage: " + str(round((self.jake_wins * 100 / total), 2)) + "%")
        print("tie percentage: " + str(round((self.ties * 100 / total), 2)) + "%")
        print("Overall tie percentage: " + str(round((self.overall_ties * 100 / total), 5)) + "%")

    def print_metadata_to_file(self, filename):
        with open(filename, "w") as outfile:
            outfile.write(PicksMetaData.get_output_header())
            for pick in sorted(self.picks, key=lambda x: (x.metaData.money_total, x.metaData.get_avg_place()), reverse=True):
                outfile.write(pick.metaData.get_file_output())

    def print_meta_data_to_json(self, filename):
        self.load_wins(CurrentYearPicks.year.wins)

        output_json = []
        for pick in sorted(self.picks, key=lambda x: (x.metaData.money_total, -1 * x.metaData.get_avg_place()), reverse=True):
            current_odds = pick.metaData.get_current_odds_json()
            currentScore = self.bracket.get_score_from_pick_values(pick.pickValues)
            current_odds["currentScore"] = currentScore
            output_json.append(current_odds)
        with open(filename, "w") as outfile:
            outfile.write(json.dumps(output_json, indent=2))

    def get_picks_metadata(self):
        metadata = list()
        for pick in self.picks:
            metadata.append(copy.copy(pick.metaData))

        return metadata

    def reset_picks_metadata(self):
        for pick in self.picks:
            if pick.metaData is not None:
                pick.metaData.reset_stats()

    def reset_bet_data(self):
        self.jake_wins = 0
        self.dad_wins = 0
        self.ties = 0
        self.overall_ties = 0
