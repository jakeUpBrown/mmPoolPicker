import os
import random
import copy

from pool_simulator.utils.FilePathConstants import FilePathConstants
from pool_simulator.Picks import Picks
from pool_simulator.PicksMetaData import PicksMetaData

expectedNames = {'bob', 'dave b.', 'drew', 'sholar', 'barb', 'neal', 'liquorman', 'dave monkey', 'purdue pete', 'chad',
                 'peninsular danny', 'gully', 'RF', 'jake', 'garret', 'josh', 'carter', 'tyler', 'random', 'random'}


class Year:

    def __init__(self, year):
        self.year = year
        self.picks = list()
        self.wins = list()
        self.averageValues = list()

    def appendPick(self, pick):
        self.picks.append(pick)

    def calcAveragePickValues(self):
        self.averageValues = list()

        num_values = len(self.picks[0].pickValues)

        for i in range(num_values):
            total = 0
            for j in range(len(self.picks)):
                total += self.picks[j].pickValues[i]

            self.averageValues.append(total / num_values)

    def setWins(self, wins):
        for winValue in wins:
            self.wins.append(int(winValue))


def get_seed_order():
    with open(os.path.abspath(FilePathConstants.get_data_file("seed-order.csv")), "r") as infile:
        return infile.readline().rstrip().split(',')


def load_my_picks():
    with open(os.path.abspath(FilePathConstants.get_data_file("my-picks.csv")), "r") as infile:
        return Picks(infile.readline().rstrip().split(','), 2019)


def load_expected_average():
    with open(os.path.abspath(FilePathConstants.get_data_file("expected-averages.csv")), "r") as infile:
        return infile.readline().rstrip().split(',')


def load_current_odds():
    current_odds_meta_data = list()
    with open(os.path.abspath(FilePathConstants.get_output_file("current-odds.csv")), "r") as infile:

        first = True

        for aline in infile:
            # skip header row
            if first:
                first = False
                continue
            current_odds_meta_data.append(PicksMetaData.from_csv(aline.rstrip().split(',')))

    return current_odds_meta_data


class PastPicks:
    nameDict = dict()

    years = []
    currentYear = None

    allPicks = []

    with open(os.path.abspath(FilePathConstants.get_data_file("past-picks.csv")), "r") as infile:
        for aline in infile:
            items = aline.rstrip().split(',')

            if items[2] == '':
                # must be a year row because the second column is blank
                if currentYear is not None:
                    years.append(currentYear)

                currentYear = Year(int(items[1]))
                continue

            if items[1] == "wins":
                currentYear.wins = items
                continue

            picks = Picks(items, currentYear.year)

            currentYear.appendPick(picks)

    if len(currentYear.picks) > 0:
        years.append(currentYear)

    for year in years:
        year.calcAveragePickValues()
        allPicks.extend(year.picks)

    @classmethod
    def get_random_other_picks_set(cls, index_to_exclude):
        sample_size = 17

        if index_to_exclude < 0 or index_to_exclude >= len(cls.allPicks):
            valid_picks = cls.allPicks
        else:
            valid_picks = copy.deepcopy(cls.allPicks)
            del valid_picks[index_to_exclude]

        sample = [
            valid_picks[i] for i in random.sample(range(len(valid_picks)), sample_size)
        ]

        return sample

    @classmethod
    def load_picks_by_index(cls, index):
        return cls.allPicks[index]

    @classmethod
    def calc_effective_values(cls):
        # get expected average
        expected_average = load_expected_average()

        for pick in cls.allPicks:
            pick.set_effective_values(expected_average)


class CurrentYearPicks:
    year = None

    allPicks = []

    with open(os.path.abspath(FilePathConstants.get_data_file("POOL19 - metrics - ThisYear.csv")), "r") as infile:
        for aline in infile:
            items = aline.rstrip().split(',')

            if items[0] == '':
                if items[1] == '':
                    break
                elif items[1] == 'wins':
                    year.setWins(items[2:])
                else:
                    year = Year(int(items[1]))
                continue

            picks = Picks(items, year.year)

            year.appendPick(picks)

    allPicks.extend(year.picks)
