from pool_simulator.Bracket import Bracket
from pool_simulator.Pool import Pool
from pool_simulator.TeamLoader import TeamInfoContainer


def build_pool():
    teams = TeamInfoContainer.create_team_instances()
    return Pool(Bracket(teams))
