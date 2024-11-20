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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if not start_date_str or not end_date_str:
        return jsonify({'error': 'Please provide both start_date and end_date in YYYY-MM-DD format'}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format'}), 400

    try:
        # get games within a specified date range
        games = Game.query.filter(Game.starts_at.between(start_date, end_date)).all()
        if not games:
            print(f"No games found between {start_date_str} and {end_date_str}")
            return jsonify({'error': 'No games found in the provided date range'}), 404

        game_ids = [game.id for game in games]
        print(f"Found games with IDs: {game_ids}")

        # check for eligible streaming packages
        filters = [StreamingOffer.game_id.in_(game_ids)]
        if live_filter is not None:
            filters.append(StreamingOffer.live == (live_filter.lower() == 'true'))
        if highlight_filter is not None:
            filters.append(StreamingOffer.highlights == (highlight_filter.lower() == 'true'))

        print(f"Filters used: {filters}") # add debugging information to view filter conditions

        offers_query = StreamingOffer.query.filter(*filters)
        compiled_query = str(offers_query.statement.compile(compile_kwargs={"literal_binds": True}))
        print(f"Compiled SQL Query: {compiled_query}")

        offers_paginated = offers_query.paginate(page=page, per_page=per_page, error_out=False)
        offers = offers_paginated.items

        if not offers:
            print(f"No streaming offers found for the given games.")
            return jsonify({'message': 'No streaming offers found in the provided data range'}), 404

        result = []
        for offer in offers:
            package = StreamingPackage.query.get(offer.streaming_package_id)
            game = Game.query.get(offer.game_id)
            result.append({
                'game_id':offer.game_id,
                'game_details':{
                    'team_home':game.team_home,
                    'team_away':game.team_away,
                    'starts_at':game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'tournament_name':game.tournament_name
                },
                'streaming_package':{
                    'streaming_package_id':package.id,
                    'name':package.name,
                    'monthly_price_cents':package.monthly_price_cents,
                    'monthly_price_yearly_subscription_in_cents':package.monthly_price_yearly_subscription_in_cents
                },
                'live':offer.live,
                'highlights':offer.highlights
            })
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error fetching streaming offers: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


