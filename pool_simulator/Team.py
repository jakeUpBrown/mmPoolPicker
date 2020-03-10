import json

class TeamInfo:
    def __init__(self, team_num, seed, team_name, adj_em, adj_t):
        self.team_num = team_num
        self.seed = seed
        self.team_name = team_name
        self.adj_em = adj_em
        self.adj_t = adj_t


class Team:
    def __init__(self, team_info):
        self.team_info = team_info
        self.wins = 0
        self.elim = False
        
    def add_game_outcome(self, won_game):
        if won_game:
            self.wins += 1
        else:
            self.elim = True

    def reset(self):
        self.wins = 0

    def get_json(self):
        teamJson = json.loads('{}')
        teamJson['id'] = self.team_info.team_num
        teamJson['seed'] = self.team_info.seed
        teamJson['name'] = self.team_info.team_name
        teamJson['isElim'] = self.elim
        teamJson['wins'] = self.wins

        return teamJson
