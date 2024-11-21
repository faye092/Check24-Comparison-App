from flask import Blueprint, jsonify, request
from models import Game
from sqlalchemy import func
from datetime import datetime
import logging

# Initialize Blueprint for games with a URL prefix
games_blueprint = Blueprint('games', __name__, url_prefix='/games')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get all games
@games_blueprint.route('/', methods=['GET'])
def get_all_games():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    if page <= 0 or per_page <= 0:
        return jsonify({'error': 'Page and per_page must be positive integers'}), 400

    games = Game.query.paginate(page=page, per_page=per_page, error_out=False)
    result = [{
        'id': game.id,
        'team_home': game.team_home,
        'team_away': game.team_away,
        'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
        'tournament_name': game.tournament_name
    } for game in games.items]
    return jsonify(result)

# Get game by team name
@games_blueprint.route('/team', methods=['GET'])
def get_games_by_team():
    try:
        team_name = request.args.get('team_name', '').strip().lower()
        if not team_name:
            return jsonify({'error': 'Team name is required'}), 400

        team_type = request.args.get('team_type', '').lower()
        if team_type not in ['home', 'away', 'both', '']:
            return jsonify({'error': "Invalid team_type. Must be 'home', 'away', or 'both'"}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        # Filter matches based on team_type
        if team_type == 'home':
            games = Game.query.filter(func.lower(Game.team_home) == team_name).paginate(page=page, per_page=per_page, error_out=False)
        elif team_type == 'away':
            games = Game.query.filter(func.lower(Game.team_away) == team_name).paginate(page=page, per_page=per_page, error_out=False)
        else:
            games = Game.query.filter(
                (func.lower(Game.team_home) == team_name) |
                (func.lower(Game.team_away) == team_name)
            ).paginate(page=page, per_page=per_page, error_out=False)

        result = [{
            'id': game.id,
            'team_home': game.team_home,
            'team_away': game.team_away,
            'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
            'tournament_name': game.tournament_name
        } for game in games.items]

        return jsonify(result) if games.items else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error fetching games for team {team_name}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Get game by tournament name
@games_blueprint.route('/tournament', methods=['GET'])
def get_games_by_tournament():
    try:
        tournament_name = request.args.get('tournament_name', '').strip().lower()
        if not tournament_name:
            return jsonify({'error': 'Tournament name is required'}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        games = Game.query.filter(func.lower(Game.tournament_name).ilike(f'%{tournament_name}%')).paginate(page=page, per_page=per_page, error_out=False)

        result = [{
            'id': game.id,
            'team_home': game.team_home,
            'team_away': game.team_away,
            'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
            'tournament_name': game.tournament_name
        } for game in games.items]

        return jsonify(result) if games.items else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error fetching games for tournament {tournament_name}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Get game by year and month
@games_blueprint.route('/by_year_month', methods=['GET'])
def get_games_by_year_month():
    try:
        year = request.args.get('year')
        month = request.args.get('month')
        if not year or not month:
            return jsonify({'error': 'Please provide both year and month'}), 400

        try:
            year = int(year)
            month = int(month)
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
        except ValueError:
            return jsonify({'error': 'Year and month must be valid integers'}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        games = Game.query.filter(Game.starts_at >= start_date, Game.starts_at < end_date).paginate(page=page, per_page=per_page, error_out=False)

        result = [{
            'id': game.id,
            'team_home': game.team_home,
            'team_away': game.team_away,
            'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
            'tournament_name': game.tournament_name
        } for game in games.items]

        return jsonify(result) if games.items else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error fetching games by year and month: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
