import pandas as pd
from package.models import *
from IPython.display import Image, HTML
from dash.dependencies import Input, Output, State
from package.queries import *
from collections import Counter
from sqlalchemy import func
import plotly.plotly as py
import plotly.graph_objs as go
import dash_table
import dash_table_experiments as dt

# from sqlalchemy import *
# from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///package/EPL_fantasy.db')

# Session = sessionmaker(bind=engine)
# session = Session()


df = pd.read_sql_table('teams', engine)

players_df = pd.DataFrame(columns= money_team_table()[0], data=money_team_table()[1])
budget_left = round(100 - players_df.cost.sum(), 2)

layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#660066"),
    titlefont=dict(color="#660066", size='14'),
    margin=dict(
        l=15,
        r=15,
        b=15,
        t=15
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#660066',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '10'

def simple_team_table():
    table_headers = Team.__table__.columns.keys()[2:-1]
    row_values = [[item.position for item in team_list()], [item.name for item in team_list()], [item.GP for item in team_list()], [item.W for item in team_list()], [item.D for item in team_list()], [item.L for item in team_list()], [item.points for item in team_list()], [item.GF for item in team_list()], [item.GA for item in team_list()], [item.GD for item in team_list()], [item.player_points for item in team_list()]]
    trace = go.Table(
    header=dict(values=table_headers),
    cells=dict(values=row_values))
    return dict(data = [trace])

def simple_player_table():
    table_headers = Player.__table__.columns.keys()[2:-2]
    slice1 = table_headers[1:]
    row_values = [[item.name for item in get_money_team_objects()], [item.team.name for item in get_money_team_objects()], [item.position for item in get_money_team_objects()], [item.cost for item in get_money_team_objects()], [item.total_points for item in get_money_team_objects()], [item.bonus for item in get_money_team_objects()], [item.minutes for item in get_money_team_objects()], [item.status for item in get_money_team_objects()], [item.roi for item in get_money_team_objects()]]
    trace = go.Table(
    header=dict(values=table_headers),
    cells=dict(values=row_values))
    return dict(data = [trace])

def generate_table(dataframe, max_rows=20):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns[2:-1]])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns[2:-1]
        ]) for i in range(min(len(dataframe), max_rows))]
    )
def build_trace_player_pts_per_team(type = 'bar', title = '<b>Cumulative Squad Fantasy Points</b>'):
    teamnames = [item.name for item in team_list()]
    team_player_points = [item.player_points for item in team_list()]
    team_player_cost = [sum([player.cost for player in item.players])*3.5 for item in team_list()]
    trace1 = dict(x = teamnames, y = team_player_points, type = type, name = 'Total Fantasy Points')
    trace2 = dict(x = teamnames, y = team_player_cost, type = type, name = 'Total Squad Cost')
    layout = go.Layout(
    title= title,
    xaxis=dict(
    tickangle = 35,
        tickfont=dict(
            size=12,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=dict(
        title='',
        titlefont=dict(
            size=12,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
)
    return dict(data = [trace1, trace2], layout = layout)

def build_trace_money_team_comparison(type = 'bar', title = "<b>AI's Smart Picks vs. The Common Folk's Picks</b>"):
    money_team_points = sum([item.total_points for item in build_team_by_roi()])
    average_joes_points = sum([item.total_points for item in build_team_by_points()])
    zach_team = 827
    trace1 = dict(x = ['Money Team'], y = [money_team_points], type = type, name = 'Money Team')
    trace2 = dict(x = ["AVG Joe's Team"], y = [average_joes_points], type = type, name = 'AVG Joe')
    trace3 = dict(x = ["Zach's Team"], y = [zach_team], type = type, name = "Zach's Team")
    layout = dict(title = title, xaxis=dict(tickfont=dict(size=16)))
    return dict(data = [trace1, trace2, trace3], layout = layout)

def money_team_composition_pie(title = '<b>Money Team Composition</b>', type = 'pie', name = 'Money Team'):
    money_team_counter = Counter([item.team.name for item in build_team_by_roi()])
    avg_joe_counter = Counter([item.team.name for item in build_team_by_points()])
    x = money_team_counter.items()
    y = avg_joe_counter.items()
    money_labels = [item[0] for item in x]
    money_values = [item[1] for item in x]
    joe_lables = [item[0] for item in y]
    joe_values= [item[1] for item in y]
    trace1 = dict(values = money_values, labels = money_labels, type = type, name = name )
    layout = dict(title = title)
    return dict(data = [trace1], layout = layout)

def avg_joe_team_composition_pie(title = '<b>AVG Joe Composition</b>', type = 'pie', name = 'AVG Joe'):
    avg_joe_counter = Counter([item.team.name for item in build_team_by_points()])
    y = avg_joe_counter.items()
    joe_labels = [item[0] for item in y]
    joe_values = [item[1] for item in y]
    trace1 = dict(values = joe_values, labels = joe_labels, type = type, name = name )
    layout = dict(title = title)
    return dict(data = [trace1], layout = layout)

def top50_roi_team_distribution(title = '<b>Top 50 ROI Players Team Distribution</b>', type = 'pie', name = 'Money Team'):
    top_50 = Counter([item.team.name for item in roi_top_players()[:50]])
    bottom_50 = Counter([item.team.name for item in roi_bottom_players()[:50]])
    x = top_50.items()
    y = bottom_50.items()
    top_labels = [item[0] for item in x]
    top_values = [item[1] for item in x]
    bottom_labels = [item[0] for item in y]
    bottom_values = [item[1] for item in y]
    trace1 = dict(values = top_values, labels = top_labels, type = type, name = name)
    trace2 = dict(values = bottom_values, labels = bottom_labels, type = type, name = name )
    layout = dict(title = title)
    return dict(data = [trace1], layout = layout)

def bottom50_roi_team_distribution(title = '<b>Bottom 50 ROI Players Team Distribution</b>', type = 'pie', name = 'Money Team'):
    top_50 = Counter([item.team.name for item in roi_top_players()[:50]])
    bottom_50 = Counter([item.team.name for item in roi_bottom_players()[:50]])
    x = top_50.items()
    y = bottom_50.items()
    top_labels = [item[0] for item in x]
    top_values = [item[1] for item in x]
    bottom_labels = [item[0] for item in y]
    bottom_values = [item[1] for item in y]
    trace1 = dict(values = top_values, labels = top_labels, type = type, name = name)
    trace2 = dict(values = bottom_values, labels = bottom_labels, type = type, name = name )
    layout = dict(title = title)
    return dict(data = [trace2], layout = layout)

def build_trace_all_players_points(title = '<b>Player Points vs Player Cost</b>', type = 'scatter', mode = 'markers'):
    list_of_player_costs = [item.cost for item in player_list()]
    list_of_player_points = [item.total_points for item in player_list()]
    player_names = [item.name for item in player_list()]
    trace1 = dict(x = list_of_player_costs, y = list_of_player_points, text = player_names, type = type, mode = mode)
    layout = dict(hovermode = 'closest', title = title, xaxis = dict(title = 'Player Cost (millions)'), yaxis = dict(title = 'Total Fantasy Points'), images= [dict(
                  source= "https://wallpapercave.com/wp/wp1830652.jpg",
                  xref= "x",
                  yref= "y",
                  x=5,
                  y= 60,
                  sizex= 6,
                  sizey= 6,
                  sizing= "stretch",
                  opacity= 0.5,
                  layer= "below")])
    return dict(data = [trace1], layout =layout)

def build_trace_top_vs_bottom_roi(type = 'bar', title = "<b>Top 20 Players vs Bottom 20 by ROI</b>"):
    roi_top_names = [item.name for item in roi_top_players()[:20]]
    roi_top_values = [item.roi for item in roi_top_players()[:20]]
    roi_bottom_names = [item.name for item in roi_bottom_players()[:20]]
    roi_bottom_values = [item.roi for item in roi_bottom_players()[:20]]
    avg_roi = 5.74
    trace1 = dict(x = roi_top_names, y = roi_top_values, type = type, name = 'Top 20 by ROI')
    trace2 = dict(x = roi_bottom_names, y = roi_bottom_values, type = type, name = 'Bottom 20 by ROI')
    trace3 = dict(x = [roi_top_names[0], roi_bottom_names[-1]], y = [avg_roi, avg_roi], type = 'scatter', mode = 'line', name = "AVG ROI")
    layout = dict(title = title, xaxis=dict(title='',  showticklabels=True, tickangle=35, tickfont=dict(family='Old Standard TT, serif', size=12, color='black')))
    return dict(data = [trace1, trace2, trace3], layout = layout)

def build_trace_avg_roi_per_team(title = "<b>Cumulative Team ROI</b>", type ='bar'):
    teamnames = [item.name for item in team_list()]
    player_count = [len(item.players) for item in team_list()]
    team_player_points = [item.player_points for item in team_list()]
    team_player_cost = [sum([player.cost for player in item.players]) for item in team_list()]
    combinedd = list(zip(team_player_points, team_player_cost))
    team_roi = [round(item[0]/item[1], 2) for item in combinedd]
    trace1 = dict(x = teamnames, y = team_roi, type = type, name = 'Team ROI')
    trace2 = dict(x = teamnames, y = player_count, type = type, name = 'Number of Players')
    layout = dict(title = title)
    return dict(data = [trace1, trace2], layout = layout)
