from flask import Flask, request, session
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from main import config


# Create and configure app object
app = Flask(__name__)
app.secret_key = 'secret?'
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database, login manager and babel objects
db = SQLAlchemy(app)
manager = LoginManager(app)
babel = Babel(app)

# Create tables
from main import models, routes
db.create_all()


# Language choice after every request
# If user have not chosen language manually, then use browser language
@babel.localeselector
def get_user_locale():
    if session.get('lang'):
        return session['lang']
    return request.accept_languages.best_match(['en', 'ru'])
