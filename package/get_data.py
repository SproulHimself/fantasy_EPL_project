import pandas as pd
from collections import defaultdict

data = pd.read_csv('./historical-performance.csv')
stats = data.to_dict('records')

players = pd.read_csv('./player-info.csv')
player_info = players.to_dict('records')


main_players = list(filter(lambda item: item['minutes'] > 300, stats))


def merge_data(dic1, dic2):
    for item in dic1:
        for x in dic2:
            if item['player_id'] == x['id']:
                item['lastname'] = x['second_name']
                item['firstname'] = x['first_name']
                item['team'] = x['team_name']

last_year = list(filter(lambda item: item['season_name'] == '2016/17', stats))
