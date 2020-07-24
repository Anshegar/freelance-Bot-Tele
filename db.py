
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from  datetime import datetime




# Create env for CRUD DB integration
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'ololo'
    return app


def create_db(app):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    Migrate(app, db)
    return db

app = create_app()
db = create_db(app)


class User(db.Model):
    __tablename__ = 'User'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    mail = db.Column(db.Text)
    chat_id = db.Column(db.Integer)
    subscribe = db.Column(db.Integer)

    def __init__(self,name,mail,chat_id,subscribe):
        self.name   = name
        self.mail   = mail
        self.chat_id = chat_id
        self.subscribe = subscribe

    def __repr__(self):
        if self.subscribe == 0:
            return f'{self.name} - {self.mail} - {self.chat_id} - Подписка не оформлена'
        else:
            return f'{self.name} - {self.mail} - {self.chat_id} - Подписка оформлена'



class Ask_for_help(db.Model):
    __tablename__ = 'Ask_for_help'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.Text)
    chat_id         = db.Column(db.Integer)
    mail            = db.Column(db.Text)
    ask_for_help    = db.Column(db.Text)
    date            = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,name,chat_id, mail,ask_for_help,date):
        self.name           = name
        self.chat_id        = chat_id
        self.mail           = mail
        self.ask_for_help   = ask_for_help
        self.date           = datetime.utcnow()

    def __repr__(self):
        return f'{self.id}-{self.name}-{self.chat_id}-{self.date}-{self.mail}:{self.ask_for_help}'
