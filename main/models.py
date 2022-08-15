from flask_login import UserMixin

from main import db, manager


class Phonebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(80))
    info = db.Column(db.String(80))

    def __init__(self, name, number, email, info):
        self.name = name
        self.number = number
        self.email = email
        self.info = info

    def toJson(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'number': self.number,
            'email': self.email,
            'additional_info': self.info
        }


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    records = db.relationship('Phonebook', backref='user', lazy=True)

    def __init__(self, login, password):
        self.login = login
        self.password = password


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
