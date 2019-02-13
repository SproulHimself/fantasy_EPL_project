# api.football-data.org/v2/competitions/PL/standings
import http.client
import requests
import json

url1 = 'api.football-data.org'

def get_table(url1):
    connection = http.client.HTTPConnection(url1)
    headers = { 'X-Auth-Token': '2a9a431414744c4a87048d64b726442f' }
    connection.request('GET', '/v2/competitions/PL/standings', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    return response

def final_teams_list(url1):
    return get_table(url1)['standings'][0]['table']

test = final_teams_list(url1)
