from flask import Blueprint, jsonify
from models import StreamingOffer

offers_blueprint = Blueprint("offers", __name__)

@offers_blueprint.route('/', methods=['GET'])
def get_offers():
    offers = StreamingOffer.query.all()
    return jsonify([{
        'id': offer.id,
        'game_id': offer.game_id,
        'streaming_package_id': offer.streaming_package_id,
        'live': offer.live,
        'highlights': offer.highlights
    }for offer in offers])