from flask import Blueprint, jsonify, request
from models import StreamingOffer, StreamingPackage, Game
from datetime import datetime
from sqlalchemy import and_

offers_blueprint = Blueprint("offers", __name__)

# get streaming packages based on the game ID, support filtering by live and highlight
@offers_blueprint.route('/game/<int:game_id>', methods=['GET'])
def get_offers_by_game(game_id):
    live_filter = request.args.get('live')
    highlight_filter = request.args.get('highlight')

    filters = [StreamingOffer.game_id == game_id]
    if live_filter is not None:
        filters.append(StreamingOffer.live == (live_filter.lower() == 'true'))
    if highlight_filter is not None:
        filters.append(StreamingOffer.highlights == (highlight_filter.lower() == 'true'))

    offers = StreamingOffer.query.filter(*filters).all()
    result = []
    for offer in offers:
        package = StreamingPackage.query.get(offer.streaming_package_id)
        result.append({
            'streaming_package_id': package.id,
            'streaming_package_name': package.name,
            'monthly_price_cents': package.monthly_price_cents,
            'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents,
            'live': offer.live,
            'highlights': offer.highlights
        })
    return jsonify(result)

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
    game_ids = [game.id for game in Game.query.filter(
        Game.starts_at.between(start_date, end_date)
    ).all()]

    if not game_ids:
        return jsonify({'error': 'No games found in the provided date range'}), 404

    # check for eligible streaming packages
    filters = [StreamingOffer.game_id.in_(game_ids)]
    if live_filter is not None:
        filters.append(StreamingOffer.live == (live_filter.lower() == 'true'))
    if highlight_filter is not None:
        filters.append(StreamingOffer.highlights == (highlight_filter.lower() == 'true'))

    offers = StreamingOffer.query.filter(*filters).all()
    result = []
    for offer in offers:
        package = StreamingPackage.query.get(offer.streaming_package_id)
        result.append({
            'game_id': offer.game_id,
            'streaming_package_id': package.id,
            'streaming_package_name': package.name,
            'monthly_price_cents': package.monthly_price_cents,
            'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents,
            'live': offer.live,
            'highlights': offer.highlights
        })
    return jsonify(result)

