from flask import Blueprint, jsonify, request
from models import StreamingOffer, StreamingPackage, Game

offers_blueprint = Blueprint("offers", __name__)

# get streaming packages based on the game ID, support filtering by live and highlight
@offers_blueprint.route('/game/<int:game_id>', methods=['GET'])
def get_offers_by_game(game_id):
    offers = StreamingOffer.query.all()
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
            'streaming_package_id':package.id,
            'streaming_package_name':package.name,
            'monthly_price_cents':package.monthly_price_cents,
            'monthly_price_yearly_subscription_in_cents':package.monthly_price_yearly_subscription_in_cents,
            'live':offer.live,
            'highlights':offer.highlights
        })
    return jsonify(result)

