from flask import Blueprint, jsonify, request
from ..services.search_service import save_search_service, recommend_packages_service
from ..utils.response_format import success_response, error_response

searches_blueprint = Blueprint('searches', __name__)

@searches_blueprint.route('/', methods=['POST'])
def save_search():

    data = request.json
    try:
        save_search_service(data)
        return success_response({"message": "Search saved successfully"})
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        return error_response(str(e), 500)

@searches_blueprint.route('/recommend', methods=['GET'])
def recommend_packages():

    user_id = request.args.get('user_id')
    if not user_id:
        return error_response("User ID is required", 400)

    try:
        result = recommend_packages_service(user_id)
        return success_response(result)
    except Exception as e:
        return error_response(str(e), 500)
