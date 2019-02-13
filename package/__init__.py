# import Flask and Dash
# import SQLAlchemy from flask_sqlalchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

#stylesheets for dash app
external_stylesheets=['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css', 'https://codepen.io/chriddyp/pen/bWLwgP.css']

# initialize new flask app
server = Flask(__name__)
# add configurations and database
server.config['DEBUG'] = True
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EPL_fantasy.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# connect flask_sqlalchemy to the configured flask app and create the Dash app
db = SQLAlchemy(server)
app = dash.Dash(__name__, server = server, url_base_pathname = '/dashboard/', external_stylesheets = external_stylesheets)


engine = create_engine('sqlite:///package/EPL_fantasy.db')

Session = sessionmaker(bind=engine)
session = Session()

#import our routes after our database has been configured
from package.dashboard import *
from package.models import *
from package.routes import *
