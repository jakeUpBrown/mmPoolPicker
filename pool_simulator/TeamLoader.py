import os
from typing import List

from pool_simulator.utils.FilePathConstants import FilePathConstants
from pool_simulator.Team import Team
from pool_simulator.Team import TeamInfo
from pool_simulator.utils import Utils


class TeamInfoContainer:
    infile = open(os.path.abspath(FilePathConstants.get_data_file("team-list.csv")), "r")

    teamInfos: List[TeamInfo] = list()

    team_num = 0

    for aline in infile:
        # csv is split into following indices:
        # 0 - seed
        # 1 - teamName
        # 2 - adjEm
        # 3 - adjT

        items = aline.split(",")

        # skip line if the first column isn't a number. That should be the seed
        # non-number probably means header row
        if not Utils.is_number(items[0]):
            continue

        newTeam = TeamInfo(team_num, int(items[0]), items[1], float(items[2]), float(items[3]))

        teamInfos.append(newTeam)

        team_num += 1

    @staticmethod
    def create_team_instances():
        teams: List[Team] = list()

        for teamInfo in TeamInfoContainer.teamInfos:
            team = Team(teamInfo)
            teams.append(team)

        return teams
