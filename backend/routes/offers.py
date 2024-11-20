from flask import Blueprint, jsonify, request, abort
from models import StreamingOffer, Game, StreamingPackage
from sqlalchemy.orm import joinedload
from sqlalchemy import func

# initialize Blueprint for offers
offers_blueprint = Blueprint("offers", __name__, url_prefix='/offers')

# 1. get streaming offers for a specific game
def get_offers_by_game(game_id):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        offers = StreamingOffer.query.options(joinedload(StreamingOffer.game)).filter_by(game_id=game_id).paginate(page=page, per_page=per_page, error_out=False)
        if not offers.items:
            return jsonify({'message':f'No streaming offers found for game ID {game_id}'}), 404
        
        # format the result to display relevant streaming offers
        result = [{
            'game_id': offer.game_id,
            'streaming_package_id': offer.streaming_package_id,
            'live': offer.live,
            'highlights': offer.highlights
        } for offer in offers.items]

        return jsonify(result)
    
    except Exception as e:
        print(f"Error fetching offers for game ID {game_id}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
# 2. get games available for a specific package
def get_games_by_package(package_id):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        offers = StreamingOffer.query.options(joinedload(StreamingOffer.game)).filter_by(streaming_package_id=package_id).paginate(page=page, per_page=per_page, error_out=False)
        if not offers.items:
            return jsonify({'message': f'No games found for streaming package ID {package_id}'}), 404
        
        # format the result to display relevant games
        result = [{
            'package_id': offer.streaming_package_id,
            'game_id': offer.game_id,
            'team_home': offer.game.team_home,
            'team_away': offer.game.team_away,
            'starts_at': offer.game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
            'tournament_name': offer.game.tournament_name,
            'live': offer.live,
            'highlights': offer.highlights
        } for offer in offers.items]
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error fetching games for streaming package ID {package_id}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
# 3.filter offers by conditions(live, highlights, etc.)
@offers_blueprint.route('/filter', methods=['GET'])
def filter_offers():
    try:
        live_only = request.args.get('live', type=bool, default=False)
        highlights_only = request.args.get('highlights', type=bool, default=False)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        # create a base query that can be extended based on request parameters
        query = StreamingOffer.query

        if live_only:
            query = query.filter_by(live=True)
        if highlights_only:
            query = query.filter_by(highlights=True)

        # execute query and load related games and packages to provide a comprehensive response
        offers = query.options(joinedload(StreamingOffer.game), joinedload(StreamingOffer.streaming_package)).paginate(page=page, per_page=per_page, error_out=False)

        if not offers.items:
            return jsonify({'message': 'No offers found for the given criteria'}), 404
        
        # format the result for display
        result = [{
            'game_id': offer.game_id,
            'team_home': offer.game.team_home,
            'team_away': offer.game.team_away,
            'starts_at': offer.game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
            'tournament_name': offer.game.tournament_name,
            'package_id': offer.streaming_package_id,
            'live': offer.live,
            'highlights': offer.highlights
        } for offer in offers.items]

        return jsonify(result)
    
    except Exception as e:
        print(f"Error filtering offers: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500



