# routes/packages.py
from flask import Blueprint, jsonify, request
from models import StreamingPackage, StreamingOffer, Game
from sqlalchemy import and_
from itertools import combinations
from datetime import datetime

packages_blueprint = Blueprint('packages', __name__)

# get the best combo which cover specific games
@packages_blueprint.route('/combo', methods=['POST'])
def get_best_combo():
    data = request.json
    game_ids = data.get('game_ids', [])
    live = data.get('live', False)
    highlight = data.get('highlight', False)
    
    # get the "year-month" information of the competition selected by the user
    games = Game.query.filter(Game.id.in_(game_ids)).all()
    if not games:
        return jsonify({'error': 'No games found for the provided game IDs'}), 404

    # group matches by year-month
    game_year_months = {}
    for game in games:
        year_month = game.starts_at.strftime("%Y-%m")
        if year_month not in game_year_months:
            game_year_months[year_month] = []
        game_year_months[year_month].append(game.id)

    # get all packages
    all_packages = StreamingPackage.query.all()
    total_monthly_cost = 0
    monthly_recommendations = []

    # process each year-month with competition and calculate the optimal combination for that month
    for year_month, month_game_ids in game_year_months.items():
        month_combinations = []

        for r in range(1, 4):  # combination quantities range from 1 to 3 streaming packages
            for package_combo in combinations(all_packages, r):
                combined_offers = []
                combined_monthly_price = 0

                for pkg in package_combo:
                    # skip free packages
                    if pkg.monthly_price_cents == 0 and pkg.monthly_price_yearly_subscription_in_cents == 0:
                        continue

                    combined_monthly_price += pkg.monthly_price_cents or 0
                    combined_offers.extend(
                        StreamingOffer.query.filter(
                            and_(StreamingOffer.streaming_package_id == pkg.id,
                                 StreamingOffer.game_id.in_(month_game_ids),
                                 (StreamingOffer.live == live if live else True),
                                 (StreamingOffer.highlights == highlight if highlight else True))
                        ).all()
                    )

                # calculate coverage
                both_coverage = {offer.game_id for offer in combined_offers if offer.live and offer.highlights}
                live_only_coverage = {offer.game_id for offer in combined_offers if offer.live and not offer.highlights}
                highlights_only_coverage = {offer.game_id for offer in combined_offers if not offer.live and offer.highlights}
                total_coverage = len(both_coverage | live_only_coverage | highlights_only_coverage)
                duplicate_services = both_coverage.intersection(live_only_coverage, highlights_only_coverage)
                duplicate_count = len(duplicate_services)

                month_combinations.append({
                    'packages': [pkg.name for pkg in package_combo],
                    'coverage_priority': {
                        'both_coverage': len(both_coverage),
                        'live_only_coverage': len(live_only_coverage),
                        'highlights_only_coverage': len(highlights_only_coverage)
                    },
                    'total_coverage': total_coverage,
                    'duplicate_count': duplicate_count,
                    'cost_cents': combined_monthly_price,
                    'year_month': year_month
                })

        # find out the optimal year-month combination (sorted by coverage and price)
        best_month_combo = sorted(
            month_combinations,
            key=lambda x: (-x['coverage_priority']['both_coverage'], 
                           -x['coverage_priority']['live_only_coverage'], 
                           -x['coverage_priority']['highlights_only_coverage'], 
                           x['duplicate_count'], 
                           x['cost_cents'])
        )[0]
        
        monthly_recommendations.append(best_month_combo)
        total_monthly_cost += best_month_combo['cost_cents']

    # compare total monthly subscription costs to total annual subscription costs
    total_annual_cost = sum(pkg.monthly_price_yearly_subscription_in_cents or float('inf') for pkg in all_packages)
    recommended_subscription_type = 'annual' if total_annual_cost / 12 < total_monthly_cost else 'monthly'
    
    # generate final recommendation
    result = {
        'primary_recommendation': None if recommended_subscription_type == 'monthly' else {
            'subscription_type': 'annual',
            'total_cost_cents': total_annual_cost,
            'details': [{'id': pkg.id, 'name': pkg.name} for pkg in all_packages]
        },
        'alternative_combinations': monthly_recommendations if recommended_subscription_type == 'monthly' else []
    }

    return jsonify(result)


