from flask import Blueprint, jsonify, request
from models import StreamingOffer, StreamingPackage, Game
from datetime import datetime
from sqlalchemy import and_

offers_blueprint = Blueprint("offers", __name__)

# get streaming packages based on date range, support filtering live broadcasts and highlights
@offers_blueprint.route('/by_date_range', methods=['GET'])
def get_offers_by_date_range():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    live_filter = request.args.get('live')
    highlight_filter = request.args.get('highlight')

    if not start_date_str or not end_date_str:
        return jsonify({'error': 'Please provide both start_date and end_date in YYYY-MM-DD format'}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format'}), 400

    # get games within a specified date range
    games = Game.query.filter(Game.starts_at.between(start_date, end_date)).all()
    if not games:
        return jsonify({'error': 'No games found in the provided date range'}), 404
    
    game_ids = [game.id for game in games]

    # check for eligible streaming packages
    filters = [StreamingOffer.game_id.in_(game_ids)]
    if live_filter is not None:
        filters.append(StreamingOffer.live == (live_filter.lower() == 'true'))
    if highlight_filter is not None:
        filters.append(StreamingOffer.highlights == (highlight_filter.lower() == 'true'))

    offers = StreamingOffer.query.filter(*filters).all()
    result = [{
        'game_id': offer.game_id,
        'streaming_package_id': offer.streaming_package_id,
        'live': offer.live,
        'highlights': offer.highlights
    } for offer in offers]
    
    return jsonify(result)

