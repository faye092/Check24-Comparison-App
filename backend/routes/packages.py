# routes/packages.py
from flask import Blueprint, jsonify, request
from models import StreamingPackage, StreamingOffer, Game
from sqlalchemy import and_
from datetime import datetime

packages_blueprint = Blueprint('packages', __name__)

# get the best package combination, using the greedy strategy
@packages_blueprint.route('/combo', methods=['POST'])
def get_best_combo():
    data = request.json
    game_ids = data.get('game_ids', [])
    live = data.get('live', False)
    highlight = data.get('highlight', False)
    
    # validate the entered contest ID
    games = Game.query.filter(Game.id.in_(game_ids)).all()
    if not games:
        return jsonify({'error': 'No games found for the provided game IDs'}), 404

    # greedy strategy: prioritize the lowest price and the package that covers the most games
    all_packages = StreamingPackage.query.all()
    selected_packages = []
    covered_games = set()
    remaining_game_ids = set(game_ids)

    while remaining_game_ids:
        best_package = None
        best_coverage = 0
        best_price = float('inf')

        # find the package that covers the most remaining matches
        for package in all_packages:
            offers = StreamingOffer.query.filter(
                and_(
                    StreamingOffer.streaming_package_id == package.id,
                    StreamingOffer.game_id.in_(remaining_game_ids),
                    (StreamingOffer.live == live if live else True),
                    (StreamingOffer.highlights == highlight if highlight else True)
                )
            ).all()

            coverage = len({offer.game_id for offer in offers})
            price = package.monthly_price_cents
            if coverage > best_coverage or (coverage == best_coverage and package.monthly_price_cents < best_price):
                best_package = package
                best_coverage = coverage
                best_price = price.monthly_price_cents
        
        if best_package is None:
            break

        selected_packages.append(best_package)
        newly_covered_games = {offer.game_id for offer in StreamingOffer.query.filter(
            and_(
                StreamingOffer.streaming_package_id == best_package.id,
                StreamingOffer.game_id.in_(remaining_game_ids),
                (StreamingOffer.live == live if live else True),
                (StreamingOffer.highlights == highlight if highlight else True)
            )
        ).all()}
        covered_games.update(newly_covered_games)
        remaining_game_ids -= newly_covered_games

    result = {
        'total_cost_cents': sum(package.monthly_price_cents for package in selected_packages),
        'selected_packages': [{'id': package.id, 'name':package.name} for package in selected_packages],
        'covered_games_count': len(covered_games)
    }

    return jsonify(result)


