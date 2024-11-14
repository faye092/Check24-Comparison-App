# routes/packages.py
from flask import Blueprint, jsonify, request
from models import StreamingPackage, StreamingOffer
from sqlalchemy import and_

packages_blueprint = Blueprint('packages', __name__)

# get the best combo which cover specific games
@packages_blueprint.route('/combo', methods=['POST'])
def get_best_combo():
    data = request.json
    game_ids = data.get('game_ids', [])
    live = data.get('live', False)
    highlight = data.get('highlight', False)
    
    # get all packages
    all_packages = StreamingPackage.query.all()
    package_combinations = []

    # Find out how many games each package covers
    for package in all_packages:
        offers = StreamingOffer.query.filter(
            and_(StreamingOffer.streaming_package_id == package.id,
                 StreamingOffer.game_id.in_(game_ids),
                 (StreamingOffer.live == live if live else True),
                 (StreamingOffer.highlights == highlight if highlight else True))
        ).all()
        covered_games = {offer.game_id for offer in offers}
        coverage_percentage = len(covered_games) / len(game_ids)  # Calculating coverage
        package_combinations.append({
            'package': package,
            'covered_games': covered_games,
            'coverage_percentage': coverage_percentage
        })

    # Sort by coverage and price, giving priority to combinations with high coverage and low price
    sorted_combinations = sorted(
        package_combinations,
        key=lambda x: (-x['coverage_percentage'], x['package'].monthly_price_cents)
    )

    # return results
    result = [{
        'id': combo['package'].id,
        'name': combo['package'].name,
        'monthly_price_cents': combo['package'].monthly_price_cents,
        'monthly_price_yearly_subscription_in_cents': combo['package'].monthly_price_yearly_subscription_in_cents,
        'coverage_percentage': combo['coverage_percentage']
    } for combo in sorted_combinations]

    return jsonify(result)
