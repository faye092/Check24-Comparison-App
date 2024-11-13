from flask import Blueprint, jsonify
from models import Game

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