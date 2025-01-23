from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    games = db.relationship('Game', back_populates='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ForeignKey to User table
    opponent_id = db.Column(db.Integer, nullable=True)  # Optional: Store opponent ID
    status = db.Column(db.String(50), nullable=False, default='ongoing')  # 'ongoing', 'completed', 'draw'
    winner_id = db.Column(db.Integer, nullable=True)  # ID of the winner
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='games')  # Relationship to User table
    moves = db.relationship('Move', back_populates='game', lazy=True)  # Relationship to Move table

    def __repr__(self):
        return f'<Game {self.id}, Player {self.player_id}, Opponent {self.opponent_id}, Status {self.status}>'

    def to_dict(self):
        return {
            "id": self.id,
            "player_id": self.player_id,
            "opponent_id": self.opponent_id,
            "status": self.status,
            "winner_id": self.winner_id,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

class Move(db.Model):
    __tablename__ = 'moves'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)  # ForeignKey to Game table
    player_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ForeignKey to User table
    position = db.Column(db.String(10), nullable=False)  # Position on the board (e.g., "A1")
    sequence = db.Column(db.Integer, nullable=False)  # Move sequence number
    symbol = db.Column(db.String(1), nullable=False)  # 'X' or 'O'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    game = db.relationship('Game', back_populates='moves')  # Relationship to Game table

    def __repr__(self):
        return f'<Move {self.id}, Game {self.game_id}, Player {self.player_id}, Position {self.position}>'

    def to_dict(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "player_id": self.player_id,
            "position": self.position,
            "sequence": self.sequence,
            "symbol": self.symbol,
            "timestamp": self.timestamp
        }
