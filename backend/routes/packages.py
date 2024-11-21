from flask import Blueprint, jsonify, request
from models import StreamingPackage
from sqlalchemy import func
import logging

# Initialize Blueprint for packages with a URL prefix
packages_blueprint = Blueprint('packages', __name__, url_prefix='/packages')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get all packages
@packages_blueprint.route('/', methods=['GET'])
def get_all_packages():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    if page <= 0 or per_page <= 0:
        return jsonify({'error': 'Page and per_page must be positive integers'}), 400

    packages = StreamingPackage.query.paginate(page=page, per_page=per_page, error_out=False)
    result = [{
        'id': package.id,
        'name': package.name,
        'monthly_price_cents': package.monthly_price_cents if package.monthly_price_cents is not None else "N/A",
        'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents,
        'yearly_price_total_cents': package.monthly_price_yearly_subscription_in_cents * 12,
        'is_free': package.monthly_price_cents == 0 and package.monthly_price_yearly_subscription_in_cents == 0,
        'provides_monthly_subscription': package.monthly_price_cents is not None,
        'provides_yearly_subscription': package.monthly_price_yearly_subscription_in_cents is not None
    } for package in packages.items]
    return jsonify(result)

# Get package by name
@packages_blueprint.route('/name', methods=['GET'])
def get_package_by_name():
    try:
        name = request.args.get('name', '').strip().lower()
        if not name:
            return jsonify({'error': 'Package name is required'}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        packages = StreamingPackage.query.filter(func.lower(StreamingPackage.name).ilike(f'%{name}%')).paginate(page=page, per_page=per_page, error_out=False)

        result = [{
            'id': package.id,
            'name': package.name,
            'monthly_price_cents': package.monthly_price_cents if package.monthly_price_cents is not None else "N/A",
            'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents,
            'yearly_price_total_cents': package.monthly_price_yearly_subscription_in_cents * 12,
            'is_free': package.monthly_price_cents == 0 and package.monthly_price_yearly_subscription_in_cents == 0,
            'provides_monthly_subscription': package.monthly_price_cents is not None,
            'provides_yearly_subscription': package.monthly_price_yearly_subscription_in_cents is not None
        } for package in packages.items]

        return jsonify(result) if packages.items else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error fetching package with name {name}: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Get free packages
@packages_blueprint.route('/free', methods=['GET'])
def get_free_packages():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        packages = StreamingPackage.query.filter(
            (StreamingPackage.monthly_price_cents == 0) &
            (StreamingPackage.monthly_price_yearly_subscription_in_cents == 0)
        ).paginate(page=page, per_page=per_page, error_out=False)

        result = [{
            'id': package.id,
            'name': package.name,
            'monthly_price_cents': package.monthly_price_cents,
            'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents,
            'yearly_price_total_cents': package.monthly_price_yearly_subscription_in_cents * 12,
            'is_free': True,
            'provides_monthly_subscription': True,
            'provides_yearly_subscription': True
        } for package in packages.items]

        return jsonify(result) if packages.items else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error fetching free packages: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Get packages with only yearly subscription
@packages_blueprint.route('/yearly_only', methods=['GET'])
def get_yearly_only_packages():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        packages = StreamingPackage.query.filter(StreamingPackage.monthly_price_cents.is_(None)).paginate(page=page, per_page=per_page, error_out=False)

        result = [{
            'id': package.id,
            'name': package.name,
            'monthly_price_cents': "N/A",
            'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents,
            'yearly_price_total_cents': package.monthly_price_yearly_subscription_in_cents * 12,
            'provides_monthly_subscription': False,
            'provides_yearly_subscription': True
        } for package in packages.items]

        return jsonify(result) if packages.items else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error fetching yearly-only packages: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Get packages with both monthly and yearly subscription
@packages_blueprint.route('/monthly_and_yearly', methods=['GET'])
def get_monthly_and_yearly_packages():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        packages = StreamingPackage.query.filter(StreamingPackage.monthly_price_cents.isnot(None)).paginate(page=page, per_page=per_page, error_out=False)

        result = [{
            'id': package.id,
            'name': package.name,
            'monthly_price_cents': package.monthly_price_cents,
            'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents,
            'yearly_price_total_cents': package.monthly_price_yearly_subscription_in_cents * 12,
            'provides_monthly_subscription': True,
            'provides_yearly_subscription': True
        } for package in packages.items]

        return jsonify(result) if packages.items else jsonify([]), 200

    except Exception as e:
        logger.error(f"Error fetching monthly and yearly packages: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
