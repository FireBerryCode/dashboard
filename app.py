# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_auth
import dash_bootstrap_components as dbc
import json

import warnings
import sqlite3
from sqlalchemy import Table, create_engine
from flask_sqlalchemy import SQLAlchemy
import configparser
import os
from flask_login import LoginManager, UserMixin, current_user

from google.cloud import ndb

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



warnings.filterwarnings("ignore")
#connect to SQLite database
#conn = sqlite3.connect('data.sqlite')
engine = create_engine('mysql+pymysql://root:smartenergyassets@127.0.0.1/users')
db = SQLAlchemy()

config = configparser.ConfigParser()
#create users class for interacting with users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(80))
Users_tbl = Table('users', Users.metadata)

server = app.server
#config the server to interact with the database
#Secret Key is used for user sessions
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:smartenergyassets@127.0.0.1/users',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db.init_app(server)

login_manager = LoginManager()
#This provides default implementations for the methods that Flask-#Login expects user objects to have
login_manager.init_app(server)
login_manager.login_view = '/login'

class Users(UserMixin, Users):
    pass

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


datastore_client = ndb.Client()


## A continuación hacemos las llamadas pertinentes a datastore para tener tanto los dispositivos como las alertas definidas por el usuario
class Dispositivo(ndb.Model):
    nombre = ndb.StringProperty()
    coordenadas = ndb.GeoPtProperty()

with datastore_client.context():
    keys = Dispositivo.query().fetch(keys_only=True)
    dispositivos = ndb.get_multi(keys)

    dispositivos_dropdown_list = []

    for item in dispositivos:
        device_dict = {"label":item.nombre, "value": item.key.id(), "coords": item.coordenadas}
        dispositivos_dropdown_list.append(device_dict)

