from flask import Blueprint, jsonify, request
from ..services.game_service import (
    get_all_games_service,
    get_games_by_team_service,
    get_games_by_tournament_service,
    get_games_by_date_service,
    get_games_by_date_range_service
)
from ..utils.response_format import success_response, error_response

games_blueprint = Blueprint('games', __name__)

@games_blueprint.route('/', methods=['GET'])
def get_all_games():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    if page <= 0 or per_page <= 0:
        return error_response("Page and per_page must be positive integers", 400)

    result = get_all_games_service(page, per_page)
    return success_response(result)


@games_blueprint.route('/team', methods=['GET'])
def get_games_by_team():
    team_name = request.args.get('team_name', '').strip()
    team_type = request.args.get('team_type', '').lower()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if not team_name:
        return error_response("Team name is required", 400)
    if team_type not in ['home', 'away', 'both', '']:
        return error_response("Invalid team_type. Must be 'home', 'away', or 'both'", 400)

    try:
        result = get_games_by_team_service(team_name, team_type, page, per_page)
        return success_response(result)
    except Exception as e:
        return error_response(str(e), 500)


@games_blueprint.route('/tournament', methods=['GET'])
def get_games_by_tournament():
    tournament_name = request.args.get('tournament_name', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if not tournament_name:
        return error_response("Tournament name is required", 400)

    try:
        result = get_games_by_tournament_service(tournament_name, page, per_page)
        return success_response(result)
    except Exception as e:
        return error_response(str(e), 500)


@games_blueprint.route('/date', methods=['GET'])
def get_games_by_date():
    date = request.args.get('date', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if not date:
        return error_response("Date is required in YYYY-MM-DD format", 400)

    try:
        result = get_games_by_date_service(date, page, per_page)
        return success_response(result)
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(str(e), 500)


@games_blueprint.route('/date-range', methods=['GET'])
def get_games_by_date_range():
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if not start_date or not end_date:
        return error_response("Both start_date and end_date are required in YYYY-MM-DD format", 400)

    try:
        result = get_games_by_date_range_service(start_date, end_date, page, per_page)
        return success_response(result)
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(str(e), 500)
