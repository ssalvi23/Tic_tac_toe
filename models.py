from werkzeug.security import check_password_hash  # Import the password checking method
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Define the method to check password
    def check_password(self, password):
        return check_password_hash(self.password, password)  # Compares hashed password

    # Relationship with Game (if needed)
    games = db.relationship('Game', backref='user', foreign_keys='Game.user_id')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player1 = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    player2 = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=True)
    board = db.Column(db.String(9), default="---------")
    current_turn = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    winner = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'player1': self.player1,
            'player2': self.player2,
            'board': self.board,
            'current_turn': self.current_turn,
            'winner': self.winner
        }
