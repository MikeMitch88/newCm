from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # Hashed password should ideally be stored
    moves = db.relationship('GameMove', backref='user', lazy=True)


class GameMove(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_row = db.Column(db.Integer, nullable=False)
    start_col = db.Column(db.Integer, nullable=False)
    end_row = db.Column(db.Integer, nullable=False)
    end_col = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # user = db.relationship('User', backref=db.backref('moves', lazy=True))