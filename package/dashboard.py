from package import app
from package.dash_funcs import *
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table_experiments as dt

# print(players_df.to_dict('records'))

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='EPL Table', style={'backgroundColor':'#D0D3D4', 'fontSize': 16, 'font-weight':'bold', 'text-align': 'center'}, children=[
        html.Div([
            html.Div([
                html.Div([
                    html.Img(src="https://i.imgur.com/YENd0zc.png", height = 650, width = 32),
                ], className="col-"),
                html.Div([
                    dash_table.DataTable(
                        id='EPL_table',
                        columns=[{"name": i.upper(), "id": i} for i in df.columns[2:-1]],
                        data=df.to_dict("rows"),
                        style_cell={'textAlign': 'center'},
                         style_header={
                             'backgroundColor': '#660066',
                             'fontWeight': 'bold',
                             'color': 'white'
                             },
                        style_data_conditional=[
                            {
                                'if': {"row_index": 0},
                                'backgroundColor': '#3D9970',
                                'color': 'white',
                            },
                            {
                                'if': {"row_index": 1},
                                'backgroundColor': '#3D9970',
                                'color': 'white',
                            },
                            {
                                'if': {"row_index": 2},
                                'backgroundColor': '#3D9970',
                                'color': 'white',
                            },
                            {
                                'if': {"row_index": 3},
                                'backgroundColor': '#33ff99',
                                'color': 'black',
                            },
                            {
                                'if': {"row_index": 4},
                                'backgroundColor': '#ffffb3',
                                'color': 'black',
                            },
                            {
                                'if': {"row_index": 17},
                                'backgroundColor': '#ff3333',
                                'color': 'white',
                            },
                            {
                                'if': {"row_index": 18},
                                'backgroundColor': '#cc0000',
                                'color': 'white',
                            },
                            {
                                'if': {"row_index": 19},
                                'backgroundColor': '#cc0000',
                                'color': 'white',
                            },

                        ],
                    )
                ], className="col")
            ], className="row")
        ], className="container")
                    ]),
        dcc.Tab(label='Team ROI Analysis',  style={'backgroundColor':'#D0D3D4', 'fontSize': 16, 'font-weight':'bold', 'text-align': 'center'}, children=[
            html.Div([
                dcc.Graph(
                    id='points per team',
                    figure= build_trace_player_pts_per_team()
                ),
                dcc.Graph(
                    id='team_roi',
                    figure= build_trace_avg_roi_per_team()
                ),
            ])
        ]),
        dcc.Tab(label='Player ROI Analysis', style={'backgroundColor':'#D0D3D4', 'fontSize': 16, 'font-weight':'bold', 'text-align': 'center'},  children=[
            html.Div([
                dcc.Graph(
                    id='example-graph',
                    figure= build_trace_all_players_points()
                ),
                dcc.Graph(
                    id='top_roi',
                    figure= build_trace_top_vs_bottom_roi()
                )
            ])
        ]),
        dcc.Tab(label='Players Team Distribution by ROI',  style={'backgroundColor':'#D0D3D4', 'fontSize': 16, 'font-weight':'bold', 'text-align': 'center'}, children=[
            html.Div([
                dcc.Graph(
                    id='top_50',
                    figure= top50_roi_team_distribution()
                ),
                dcc.Graph(
                    id='bottom_50',
                    figure= bottom50_roi_team_distribution()
                )
            ])
        ]),
        dcc.Tab(label='Fantasy Teams Comparison', style={'backgroundColor':'#D0D3D4', 'fontSize': 16, 'font-weight':'bold', 'text-align': 'center'}, children=[
        html.Div([
                dcc.Graph(
                    id='example-graph-2',
                    figure= build_trace_money_team_comparison(),
                    className = "twelve columns"),
                    ], className ='row'),
        html.Div([
                dcc.Graph(
                    id='graph-3',
                    figure= money_team_composition_pie(),
                    className = "six columns"),
                dcc.Graph(
                    id='avg_joe_pie',
                    figure= avg_joe_team_composition_pie(),
                    className = "six columns"),
                    ], className ='row'),
                ]),
dcc.Tab(label='Money Team Stats', style={'backgroundColor':'#D0D3D4', 'fontSize': 16, 'font-weight':'bold', 'text-align': 'center'}, children=[
    html.Div([
        html.Div([
            html.H1(children = "Money Team Fantasy View",
                    style={'backgroundColor':'#350d2e', 'color': 'white', 'fontSize': 22, 'font-weight':'bold', 'text-align': 'center', 'marginBottom': 10, 'marginTop': 12}, className = "six columns"),
            html.H1(children = "Money Team Player Stats",
                    style={'backgroundColor':'#350d2e', 'color': 'white', 'fontSize': 22, 'font-weight':'bold', 'text-align': 'center', 'marginBottom': 10, 'marginTop': 12}, className = "six columns")
                    ], className = 'row'),
        # Selectors
        html.Div([
            html.H1(children = "Remaining Bugdet:   " + str(budget_left) + "M",
                    style={'color': '#350d2e', 'fontSize': 20, 'font-weight':'bold', 'text-align': 'center', 'marginBottom': 10, 'marginTop': 12}, className = "six columns"),
            dcc.Checklist(id = 'positions',
                        options=[
                            {'label': 'Goalkeepers', 'value': 'Goalkeeper'},
                            {'label': 'Defenders', 'value': 'Defender'},
                            {'label': 'Midfielders', 'value': 'Midfielder'},
                            {'label': 'Forwards', 'value': 'Forward'},
                        ],
                        values=['Goalkeeper', 'Defender', "Midfielder",  'Forward'],
                        labelStyle={'display': 'inline-block'},
                        style={'margin': 10, 'color': 'black', 'text-align': 'center', 'fontSize': 20},
                        className='six columns')
                        ], className = 'row'),

        html.Div([
            html.Img(src="https://i.imgur.com/tfXTHvB.png", height = 620, width = 320, className="six columns"),
            html.Div([
                dt.DataTable(
                    rows=players_df.to_dict('records'),
                    columns=players_df.columns,
                    min_height=580,
                    # row_selectable=True,
                    # filterable=True,
                    # sortable=True,
                    selected_row_indices=[],
                    id='Players'),
                     ],
                style = layout_table,
                className="six columns"
                ),
            #                 style_cell={'textAlign': 'center'},
            #                  style_header={'backgroundColor': '#660066','fontWeight': 'bold', 'color': 'white'}, className="six columns")
            ], className = 'row')
            ])
        ]),
    ])
])

@app.callback(
    Output('Players', 'rows'),
     [Input('positions', 'values')])
def update_selected_row_indices(position):
    map_aux = players_df.copy()

    # Position filter
    map_aux = map_aux[map_aux["position"].isin(position)]
    rows = map_aux.to_dict('records')
    return rows


# @app.callback(
#     Output('Players', 'rows'),
#      [Input('positions', 'values')])
# def update_selected_row_indices(position):
#     map_aux = players_df.copy()
#
#     # Position filter
#     map_aux = map_aux[map_aux["position"].isin(position)]
#     rows = map_aux.to_dict('records')
#     return rows

# if __name__ == '__main__':
#     app.run_server(debug=True)

#
# app.layout = html.Div(children=[
#     html.H4(children='Premier League Table'),
#     generate_table(df)
# ])
#         html.Div([
#             html.Img(src="https://i.imgur.com/tfXTHvB.png", height = 620, width = 320, className="six columns"),
#             html.Div([dash_table.DataTable(
#                     data=[{}],
#                     columns=players_df.columns,
#                     id='Players'),
#             ],
#             style = layout_table,
#             className="six columns"
#         ),
#             ], className = 'row')
#     ])
# ]),
#     ])
# ])
