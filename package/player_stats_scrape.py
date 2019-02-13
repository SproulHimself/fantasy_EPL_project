import json
import requests
from models import *
from EPL_table_scrape import test


url = "https://fantasy.premierleague.com/drf/bootstrap-static"

def get_json_data(url):
    response = requests.get(url)
    jobs = response.json()
    return jobs

#filter out players with less than 330
all_players = get_json_data(url)['elements']
all_teams = get_json_data(url)['teams']
positions = get_json_data(url)['element_types']

main_players = list(filter(lambda player: player['minutes'] > 330, all_players))

def team_code(test, all_teams):
    teams = all_teams.copy()
    for item in test:
        for team in teams:
            if item['team']['id'] == 65 and team['code'] == 43:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 64 and team['code'] == 14:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 61 and team['code'] == 8:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 73 and team['code'] == 6:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 57 and team['code'] == 3:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 1044 and team['code'] == 91:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 346 and team['code'] == 57:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 66 and team['code'] == 1:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 62 and team['code'] == 11:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 338 and team['code'] == 13:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 76 and team['code'] == 39:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 397 and team['code'] == 36:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 563 and team['code'] == 21:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 67 and team['code'] == 4:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 328 and team['code'] == 90:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 354 and team['code'] == 31:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 340 and team['code'] == 20:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 715 and team['code'] == 97:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 394 and team['code'] == 38:
                team['name'] = item['team']['name']
            elif item['team']['id'] == 63 and team['code'] == 54:
                team['name'] = item['team']['name']
    return teams

all_teams_new = team_code(test, all_teams)

def attach_team_and_position(main_players, all_teams_new, positons):
    players = main_players.copy()
    for team in all_teams_new:
        for player in players:
            if team['code'] == player['team_code']:
                player['team_name'] = team['name']
    for position in positions:
        for player in players:
            if position['id'] == player['element_type']:
                player['position'] = position['singular_name']
    for player in players:
        if player['status'] == "a":
            player['status'] = "available"
        elif player['status'] == "d":
            player['status'] = "doubtful"
        elif player['status'] == "i":
            player['status'] = "injured"
        elif player['status'] == "s":
            player['status'] = "suspended"
    return players

player_positions_teams = attach_team_and_position(main_players, all_teams, positions)

def final_players_list(player_positions_teams):
    players = player_positions_teams.copy()
    empty = []
    for player in players:
        stats = dict(team_code = player['team_code'],
        team_name = player['team_name'],
        name = player['first_name'] + " " + player['second_name'],
        status = player['status'],
        position = player['position'],
        cost = (player['now_cost'])/10,
        total_points = player['total_points'],
        roi = round((player['total_points'] / player['now_cost'])*10, 2),
        bonus = player['bonus'],
        red_cards = player['red_cards'],
        minutes = player['minutes'],
        transfers_out = player['transfers_out'],
        transfers_in = player['transfers_in'])
        empty.append(stats)
    return empty
