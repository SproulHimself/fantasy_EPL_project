from flask import render_template, jsonify, json
from package.models import *
from package import server
from package import app
from package.queries import *
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


#  let's define out '/go-to-dashboard' route here:
@app.server.route('/go-to-dashboard')
def dashboard():
    return app.index()


@app.server.route('/api/teams')
def team_index():
    all_teams = db.session.query(Team).all()
    all_teams_dicts = [team.to_dict() for team in all_teams]
    return jsonify(all_teams_dicts)

@app.server.route('/api/players')
def player_index():
    all_players = db.session.query(Player).all()
    all_players_dicts = [player.to_dict() for player in all_players]
    return jsonify(all_players_dicts)



@app.server.route('/html/epl_table')
def html_epl_table():
    teams = team_list()
    columns = Team.__table__.columns.keys()
    return render_template('epl_table.html', teams = teams, columns = columns)
