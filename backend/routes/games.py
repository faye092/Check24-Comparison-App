from flask import Blueprint, jsonify, request, abort
from models import Game
from sqlalchemy import func
from datetime import datetime

games_blueprint = Blueprint('games', __name__)

# get all games
@games_blueprint.route('/all', methods=['GET'])
def get_all_games():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
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
    try:
        team_name = team_name.strip().lower() # remove whitespace and convert to lowercase
        games = Game.query.filter(
            (func.lower(Game.team_home) == team_name) | 
            (func.lower(Game.team_away) == team_name)
        ).all()

        if not games:
            return jsonify({'message':f'No games found for team {team_name}'}), 404
        
        result = [{
            'id': game.id,
            'team_home': game.team_home,
            'team_away': game.team_away,
            'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
            'tournament_name': game.tournament_name
        } for game in games]

        return jsonify(result)
    
    except Exception as e:
        print(f"Error fetching games for team {team_name}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# get game by tournament name
@games_blueprint.route('/tournament/<tournament_name>', methods=['GET'])
def get_games_by_tournament(tournament_name):
    try:
        tournament_name = tournament_name.strip().lower() # remove whitespace and convert to lowercase
        games = Game.query.filter(func.lower(Game.tournament_name) == tournament_name).all()
        if not games:
            return jsonify({'message':f'No games found for tournament {tournament_name}'}), 404
        result = [{
            'id': game.id,
            'team_home': game.team_home,
            'team_away': game.team_away,
            'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
            'tournament_name': game.tournament_name
        } for game in games]
        return jsonify(result)

    except Exception as e:
        print(f"Error fetching games for tournament {tournament_name}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# get game by month-year, as that's relate to the subcription
@games_blueprint.route('/by_year_month', methods=['GET'])
@games_blueprint.route('/by_year_month', methods=['GET'])
def get_games_by_year_month():
    try:
        year = request.args.get('year')
        month = request.args.get('month')

        if not year or not month:
            return jsonify({'error': 'Please provide both year and month'}), 400

        games = Game.query.filter(
            func.strftime('%Y', Game.starts_at) == year,
            func.strftime('%m', Game.starts_at) == month
        ).all()

        if not games:
            return jsonify({'message': f'No games found for {year}-{month}'}), 404

        result = [{
            'id': game.id,
            'team_home': game.team_home,
            'team_away': game.team_away,
            'starts_at': game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
            'tournament_name': game.tournament_name
        } for game in games]

        return jsonify(result)

    except Exception as e:
        print(f"Error fetching games by year and month: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
