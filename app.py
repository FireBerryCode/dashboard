# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_auth
import dash_bootstrap_components as dbc
import plotly.express as px
import json

import warnings
import sqlite3
from sqlalchemy import Table, create_engine
from flask_sqlalchemy import SQLAlchemy
import configparser
import os
from flask_login import LoginManager, UserMixin


external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



warnings.filterwarnings("ignore")
#connect to SQLite database
conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()

config = configparser.ConfigParser()
#create users class for interacting with users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
Users_tbl = Table('users', Users.metadata)

server = app.server
#config the server to interact with the database
#Secret Key is used for user sessions
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db.init_app(server)

login_manager = LoginManager()
#This provides default implementations for the methods that Flask-#Login expects user objects to have
login_manager.init_app(server)
class Users(UserMixin, Users):
    pass

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))