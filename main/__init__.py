from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from main import config

app = Flask(__name__)
app.secret_key = 'secret?'
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from main import models, routes
db.create_all()
