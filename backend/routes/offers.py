from flask import Blueprint, jsonify, request
from models import StreamingOffer, Game, StreamingPackage
from sqlalchemy import func
import logging

# Initialize Blueprint for offers with a URL prefix
offers_blueprint = Blueprint('offers', __name__, url_prefix='/offers')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get all offers
@offers_blueprint.route('/', methods=['GET'])
def get_all_offers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    if page <= 0 or per_page <= 0:
        return jsonify({'error': 'Page and per_page must be positive integers'}), 400

    offers = StreamingOffer.query.paginate(page=page, per_page=per_page, error_out=False)
    result = [{
        'id': offer.id,
        'game_id': offer.game_id,
        'streaming_package_id': offer.streaming_package_id,
        'live': offer.live,
        'highlights': offer.highlights,
        'game_details': {
            'team_home': offer.game.team_home,
            'team_away': offer.game.team_away,
            'starts_at': offer.game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
            'tournament_name': offer.game.tournament_name
        },
        'package_details': {
            'name': offer.package.name,
            'monthly_price_cents': offer.package.monthly_price_cents,
            'monthly_price_yearly_subscription_in_cents': offer.package.monthly_price_yearly_subscription_in_cents
        }
    } for offer in offers.items]
    return jsonify(result)

# Get offers by game name
@offers_blueprint.route('/by_game_name', methods=['GET'])
def get_offers_by_game_name():
    try:
        tournament_name = request.args.get('tournament_name', '').strip().lower()
        team_home = request.args.get('team_home', '').strip().lower()
        team_away = request.args.get('team_away', '').strip().lower()
        if not tournament_name and not team_home and not team_away:
            return jsonify({'error': 'At least one of tournament_name, team_home, or team_away is required'}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        query = Game.query
        if tournament_name:
            query = query.filter(func.lower(Game.tournament_name).ilike(f'%{tournament_name}%'))
        if team_home:
            query = query.filter(func.lower(Game.team_home).ilike(f'%{team_home}%'))
        if team_away:
            query = query.filter(func.lower(Game.team_away).ilike(f'%{team_away}%'))

        games = query.paginate(page=page, per_page=per_page, error_out=False)
        offers = StreamingOffer.query.filter(StreamingOffer.game_id.in_([game.id for game in games.items])).all()

        result = [{
            'id': offer.id,
            'live': offer.live,
            'highlights': offer.highlights,
            'game_details': {
                'team_home': offer.game.team_home,
                'team_away': offer.game.team_away,
                'starts_at': offer.game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
                'tournament_name': offer.game.tournament_name
            },
            'package_details': {
                'name': offer.package.name,
                'monthly_price_cents': offer.package.monthly_price_cents,
                'monthly_price_yearly_subscription_in_cents': offer.package.monthly_price_yearly_subscription_in_cents
            }
        } for offer in offers]

        return jsonify(result) if offers else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error fetching offers by game name: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Get offers by package name
@offers_blueprint.route('/by_package_name', methods=['GET'])
def get_offers_by_package_name():
    try:
        package_name = request.args.get('package_name', '').strip().lower()
        if not package_name:
            return jsonify({'error': 'Package name is required'}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        packages = StreamingPackage.query.filter(func.lower(StreamingPackage.name).ilike(f'%{package_name}%')).paginate(page=page, per_page=per_page, error_out=False)
        offers = StreamingOffer.query.filter(StreamingOffer.streaming_package_id.in_([package.id for package in packages.items])).all()

        result = [{
            'id': offer.id,
            'live': offer.live,
            'highlights': offer.highlights,
            'game_details': {
                'team_home': offer.game.team_home,
                'team_away': offer.game.team_away,
                'starts_at': offer.game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
                'tournament_name': offer.game.tournament_name
            },
            'package_details': {
                'name': offer.package.name,
                'monthly_price_cents': offer.package.monthly_price_cents,
                'monthly_price_yearly_subscription_in_cents': offer.package.monthly_price_yearly_subscription_in_cents
            }
        } for offer in offers]

        return jsonify(result) if offers else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error fetching offers by package name: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Search offers by game and package name
@offers_blueprint.route('/search', methods=['GET'])
def search_offers():
    try:
        tournament_name = request.args.get('tournament_name', '').strip().lower()
        team_home = request.args.get('team_home', '').strip().lower()
        team_away = request.args.get('team_away', '').strip().lower()
        package_name = request.args.get('package_name', '').strip().lower()

        if not (tournament_name or team_home or team_away or package_name):
            return jsonify({'error': 'At least one search parameter is required'}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        game_query = Game.query
        if tournament_name:
            game_query = game_query.filter(func.lower(Game.tournament_name).ilike(f'%{tournament_name}%'))
        if team_home:
            game_query = game_query.filter(func.lower(Game.team_home).ilike(f'%{team_home}%'))
        if team_away:
            game_query = game_query.filter(func.lower(Game.team_away).ilike(f'%{team_away}%'))

        games = game_query.all()
        game_ids = [game.id for game in games]

        package_query = StreamingPackage.query
        if package_name:
            package_query = package_query.filter(func.lower(StreamingPackage.name).ilike(f'%{package_name}%'))

        packages = package_query.all()
        package_ids = [package.id for package in packages]

        offers_query = StreamingOffer.query
        if game_ids:
            offers_query = offers_query.filter(StreamingOffer.game_id.in_(game_ids))
        if package_ids:
            offers_query = offers_query.filter(StreamingOffer.streaming_package_id.in_(package_ids))

        offers = offers_query.paginate(page=page, per_page=per_page, error_out=False)
        result = [{
            'id': offer.id,
            'live': offer.live,
            'highlights': offer.highlights,
            'game_details': {
                'team_home': offer.game.team_home,
                'team_away': offer.game.team_away,
                'starts_at': offer.game.starts_at.strftime("%Y-%m-%d %H:%M:%S"),
                'tournament_name': offer.game.tournament_name
            },
            'package_details': {
                'name': offer.package.name,
                'monthly_price_cents': offer.package.monthly_price_cents,
                'monthly_price_yearly_subscription_in_cents': offer.package.monthly_price_yearly_subscription_in_cents
            }
        } for offer in offers.items]

        return jsonify(result) if offers.items else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error searching offers: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
