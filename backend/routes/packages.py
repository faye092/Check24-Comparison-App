from flask import Blueprint, jsonify, request
from models import StreamingPackage, StreamingOffer
from sqlalchemy import and_

packages_blueprint = Blueprint('packages', __name__)

# get all packages
@packages_blueprint.route('/', methods=['GET'])
def get_all_packages():
    packages = StreamingPackage.query.all()
    result = [{
        'id': package.id,
        'name': package.name,
        'monthly_price_cents': package.monthly_price_cents,
        'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents
    } for package in packages]
    return jsonify(result)

# get the best combo which cover specific games
@packages_blueprint.route('/combo', methods=['POST'])
def get_best_combo():
    data = request.json
    game_ids = data.get('game_ids',[])

    # search the combe which cover all selected games
    packages = StreamingPackage.query.join(StreamingOffer).filter(
        StreamingOffer.game_id.in_(game_ids),
        StreamingOffer.live == True
    ).all()

    # return all combos which commit the requirements
    result = [{
        'id': package.id,
        'name': package.name,
        'monthly_price_cents': package.monthly_price_cents,
        'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents
    } for package in packages]
    return jsonify(result)