from flask import Blueprint, jsonify, request
from models import Game
from datetime import datetime
from sqlalchemy import or_, and_

games_blueprint = Blueprint('games', __name__)

# get all games
@games_blueprint.route('/', methods=['GET'])
def get_all_games():
    games = Game.query.all()
    result = [{
        'id': game.id,
        'team_home': game.team_home,
        'team_away': game.team_away,
        'starts_at': game.starts_at,
        'tournament_name': game.tournament_name
    } for game in games]
    return jsonify(result)


# get game by team name
@games_blueprint.route('/team/<team_name>', methods=['GET'])
def get_games_by_team(team_name):
    games = Game.query.filter((Game.team_home == team_name) | (Game.team_away == team_name)).all()
    result = [{
        'id': game.id,
        'team_home': game.team_home,
        'team_away': game.team_away,
        'starts_at': game.starts_at,
        'tournament_name': game.tournament_name
    }for game in games]
    return jsonify(result)

# get game by tournament name
@games_blueprint.route('/tournament/<tournament_name>', methods=['GET'])
def get_games_by_tournament(tournament_name):
    games = Game.query.filter(Game.tournament_name == tournament_name).all()
    result = [{
        'id': game.id,
        'team_home': game.team_home,
        'team_away': game.team_away,
        'starts_at': game.starts_at,
        'tournament_name': game.tournament_name
    }for game in games]
    return jsonify(result)

# get game by month-year, as that's relate to the subcription
@games_blueprint.route('/by_year_month', methods=['GET'])
def get_games_by_year_month():
    games = Game.query.all()
    games_by_year_month = {}
    for game in games:
        year_month = game.starts_at.strftime("%Y-%m")  # Group by "year-month"
        if year_month not in games_by_year_month:
            games_by_year_month[year_month] = []
        games_by_year_month[year_month].append({
            'id': game.id,
            'team_home': game.team_home,
            'team_away': game.team_away,
            'starts_at': game.starts_at,
            'tournament_name': game.tournament_name
        })
    return jsonify(games_by_year_month)