from package import db


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key = True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', back_populates = 'players')
    team_code = db.Column(db.Integer)
    name = db.Column(db.String)
    position = db.Column(db.String)
    cost = db.Column(db.Float)
    total_points = db.Column(db.Integer)
    roi = db.Column(db.Float)
    bonus = db.Column(db.Integer)
    red_cards = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    status = db.Column(db.String)
    transfers_out = db.Column(db.Integer)
    transfers_in = db.Column(db.Integer)
    def to_dict(self):
        player_d = {'id': self.id, 'name': self.name, 'position': self.position, 'cost': self.cost, 'total_points': self.total_points, 'roi': self.roi, 'bonus': self.bonus, 'red_cards': self.red_cards, 'minutes': self.minutes, 'status': self.status, 'transfers_out': self.transfers_out, 'transfers_in': self.transfers_in, 'team' : self.team.name }
        return player_d


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key = True)
    # table_id = db.Column(db.Integer, Foreign_Key('epl_table.id'))
    code = db.Column(db.Integer)
    position = db.Column(db.Integer)
    name = db.Column(db.String)
    GP = db.Column(db.Integer)
    W = db.Column(db.Integer)
    D = db.Column(db.Integer)
    L = db.Column(db.Integer)
    points = db.Column(db.Integer)
    GF = db.Column(db.Integer)
    GA = db.Column(db.Integer)
    GD = db.Column(db.Integer)
    player_points = db.Column(db.Integer)
    logo = db.Column(db.String)
    players = db.relationship('Player', back_populates = 'team')
    def to_dict(self):
        team_d = {'id': self.id, 'name': self.name, 'position': self.position, 'points': self.points, 'GP': self.GP, 'W': self.W, 'D': self.D, 'L': self.L, 'GF': self.GF, 'GA': self.GA, 'GD': self.GD, 'player_points': self.player_points, 'logo': self.logo,}
        return team_d

db.create_all()
# # created and seeded tables
# def inst_teams():
#     teams = final_teams_list(url1)
#     empty = []
#     for item in teams:
#         team = Team(position = item['position'], name = item['team']['name'], logo = item['team']['crestUrl'], GP = item['playedGames'], W = item['won'], D = item['draw'], L = item['lost'], points = item['points'], GF = item['goalsFor'], GA = item['goalsAgainst'], GD = item['goalDifference'], player_points = 0, players = [])
#         empty.append(team)
#     return empty
#
# def inst_players_and_teams():
#     players = final_players_list(player_positions_teams)
#     teams = inst_teams()
#     players_final = []
#     teams_final = []
#     # pdb.set_trace()
#     for team in teams:
#         for item in players:
#             if team.name == item['team_name']:
#                 player = Player(team = team, name = item['name'], position = item['position'], cost = item['cost'], total_points = item['total_points'], roi = item['roi'], bonus = item['bonus'], red_cards = item['red_cards'], minutes = item['minutes'], status = item['status'], transfers_out = item['transfers_out'], transfers_in = item['transfers_in'])
#                 team.players.append(player)
#                 team.player_points += item['total_points']
#                 players_final.append(player)
#                 if team not in teams_final:
#                     teams_final.append(team)
#     return (teams_final, players_final)
#
# team_results = inst_players_and_teams()[0]
# player_results = inst_players_and_teams()[1]
