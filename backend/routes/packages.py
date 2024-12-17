from flask import Blueprint, request
from ..services.package_service import (
    get_all_packages_service,
    search_packages_service,
    get_optimal_packages_by_filters
)
from ..utils.response_format import success_response, error_response

packages_blueprint = Blueprint('packages', __name__)

@packages_blueprint.route('/', methods=['GET'])
def get_all_packages():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if page <= 0 or per_page <= 0:
        return error_response("Page and per_page must be positive integers", 400)

    try:
        result = get_all_packages_service(page, per_page)
        return success_response(result)
    except Exception as e:
        return error_response(str(e), 500)


@packages_blueprint.route('/search', methods=['GET'])
def search_packages():

    name = request.args.get('name', '').strip().lower()
    subscription_type = request.args.get('type', '').strip().lower()

    try:
        result = search_packages_service(name, subscription_type)
        return success_response(result)
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(str(e), 500)


@packages_blueprint.route('/optimal', methods=['POST'])
def find_optimal_packages():

    data = request.json
    tournament_name = data.get("tournament_name", "").strip()
    team_name = data.get("team_name", "").strip()
    date = data.get("date", "").strip()

    if not tournament_name and not team_name and not date:
        return error_response("Please provide at least one filter: tournament_name, team_name, or date.", 400)

    try:
        result = get_optimal_packages_by_filters(tournament_name, team_name, date)
        return success_response(result)
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(str(e), 500)
