#manage database and users
import sqlite3
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin



conn = sqlite3.connect('data.sqlite')
#connect to the database
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()
#class for the table Users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
Users_tbl = Table('users', Users.metadata)
#fuction to create table using Users class
def create_users_table():
    Users.metadata.create_all(engine)
#create the table
create_users_table()

import pandas as pd
c = conn.cursor()
df = pd.read_sql('select * from users', conn)
df