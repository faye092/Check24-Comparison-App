from flask import Blueprint, jsonify, request
from models import Game
from sqlalchemy import or_
from datetime import datetime

games_blueprint = Blueprint('games', __name__)

# get all games
@games_blueprint.route('/', methods=['GET'])
def get_all_games():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    games = Game.query.paginate(page=page, per_page=per_page, error_out=False)
    result = [{
        'id': game.id,
        'team_home': game.team_home,
        'team_away': game.team_away,
        'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
        'tournament_name': game.tournament_name
    } for game in games.items]
    return jsonify(result)


# get game by team name
@games_blueprint.route('/team/<team_name>', methods=['GET'])
def get_games_by_team(team_name):
    games = Game.query.filter((Game.team_home == team_name) | (Game.team_away == team_name)).all()
    result = [{
        'id': game.id,
        'team_home': game.team_home,
        'team_away': game.team_away,
        'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
        'tournament_name': game.tournament_name
    }for game in games.items]
    return jsonify(result)

# get game by tournament name
@games_blueprint.route('/tournament/<tournament_name>', methods=['GET'])
def get_games_by_tournament(tournament_name):
    games = Game.query.filter(Game.tournament_name == tournament_name).all()
    result = [{
        'id': game.id,
        'team_home': game.team_home,
        'team_away': game.team_away,
        'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
        'tournament_name': game.tournament_name
    }for game in games.items]
    return jsonify(result)

# get game by month-year, as that's relate to the subcription
@games_blueprint.route('/by_year_month', methods=['GET'])
def get_games_by_year_month():
    year_month = request.args.get('year_month')
    if not year_month:
        return jsonify({'error': 'Please provide year_month in YYYY-MM format'}), 400
    
    try:
        year, month = map(int, year_month.split('-'))
        games = Game.query.filter(
            Game.starts_at.between(datetime(year, month, 1), datetime(year, month+1, 1))
        ).all()
    except ValueError:
        return jsonify({'error': 'Invalid year-month format'}), 400
    
    result = [{
        'id': game.id,
        'team_home': game.team_home,
        'team_away': game.team_away,
        'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
        'tournament_name': game.tournament_name
    } for game in games]
    return jsonify(result)