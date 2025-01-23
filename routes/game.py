from contextlib import _RedirectStream
from flask import Blueprint, jsonify, session, request
from flask_login import login_required  # Correct import
from models import db, Game, Move, User  # Removed login_required
from datetime import datetime
from flask import render_template


game_bp = Blueprint('game', __name__)

@game_bp.route('/create', methods=['POST'])
@login_required
def create_game():
    try:
        data = request.get_json()
        opponent_username = data.get('opponent')
        
        opponent = User.query.filter_by(username=opponent_username).first()
        if not opponent:
            return jsonify({"error": "Opponent not found"}), 404

        new_game = Game(
            player_id=session['user_id'],
            opponent_id=opponent.id,
            status='ongoing'
        )
        db.session.add(new_game)
        db.session.commit()

        # Redirect to the game page after creating the game
        return _RedirectStream(url_for('game.game_page', game_id=new_game.id))  # Redirect to game.html

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Add a route for serving the game page (game.html)
@game_bp.route('/game/<int:game_id>', methods=['GET'])
@login_required
def game_page(game_id):
    # You can pass game data or any necessary context here
    game = Game.query.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    return render_template('game.html', game=game)  # Render the game.html template with game data


@game_bp.route('/move', methods=['POST'])
@login_required
def make_move():
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        position = data.get('position')
        symbol = data.get('symbol')

        game = Game.query.get(game_id)
        if not game:
            return jsonify({"error": "Game not found"}), 404

        if game.status != 'ongoing':
            return jsonify({"error": "Game is already completed"}), 400

        # Verify it's the player's turn
        last_move = Move.query.filter_by(game_id=game_id).order_by(Move.sequence.desc()).first()
        sequence = 1 if not last_move else last_move.sequence + 1

        new_move = Move(
            game_id=game_id,
            player_id=session['user_id'],
            position=position,
            sequence=sequence,
            symbol=symbol
        )
        db.session.add(new_move)
        db.session.commit()

        return jsonify({
            "message": "Move recorded successfully",
            "move": new_move.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@game_bp.route('/end', methods=['POST'])
@login_required
def end_game():
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        winner_id = data.get('winner_id')
        status = data.get('status')  # 'completed' or 'draw'

        game = Game.query.get(game_id)
        if not game:
            return jsonify({"error": "Game not found"}), 404

        game.status = status
        game.winner_id = winner_id
        game.completed_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "message": "Game ended successfully",
            "game": game.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@game_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    try:
        user_id = session['user_id']
        games = Game.query.filter(
            ((Game.player_id == user_id) | (Game.opponent_id == user_id)) &
            (Game.status != 'ongoing')
        ).order_by(Game.created_at.desc()).all()

        return jsonify({
            "games": [game.to_dict() for game in games]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@game_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    try:
        user_id = session['user_id']
        games = Game.query.filter(
            ((Game.player_id == user_id) | (Game.opponent_id == user_id)) &
            (Game.status != 'ongoing')
        ).all()

        stats = {
            'total_games': len(games),
            'wins': len([g for g in games if g.winner_id == user_id]),
            'losses': len([g for g in games if g.winner_id and g.winner_id != user_id]),
            'draws': len([g for g in games if g.status == 'draw'])
        }

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500