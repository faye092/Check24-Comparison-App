from flask import Blueprint, jsonify, request
from models import StreamingPackage
import logging

packages_blueprint = Blueprint('packages', __name__, url_prefix='/packages')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@packages_blueprint.route('/', methods=['GET'])
def get_all_packages():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        if page <= 0 or per_page <= 0:
            return jsonify({'error': 'Page and per_page must be positive integers'}), 400

        packages = StreamingPackage.query.paginate(page=page, per_page=per_page, error_out=False)
        result = [{
            'name': package.name,
            'monthly_price_cents': package.monthly_price_cents,
            'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents
        } for package in packages.items]
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error fetching packages: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@packages_blueprint.route('/search', methods=['GET'])
def search_packages():
    try:
        name = request.args.get('name', '').strip().lower()
        subscription_type = request.args.get('type', '').strip().lower()  # free, yearly_only, full
        
        query = StreamingPackage.query
        
        if name:
            query = query.filter(StreamingPackage.name.ilike(f'%{name}%'))
        
        if subscription_type == 'free':
            query = query.filter(
                StreamingPackage.monthly_price_cents == 0,
                StreamingPackage.monthly_price_yearly_subscription_in_cents == 0
            )
        elif subscription_type == 'yearly_only':
            query = query.filter(
                StreamingPackage.monthly_price_cents.is_(None),
                StreamingPackage.monthly_price_yearly_subscription_in_cents > 0
            )
        elif subscription_type == 'full':
            query = query.filter(
                StreamingPackage.monthly_price_cents > 0,
                StreamingPackage.monthly_price_yearly_subscription_in_cents > 0
            )

        packages = query.order_by(
            StreamingPackage.monthly_price_yearly_subscription_in_cents
        ).all()
        
        result = []
        for package in packages:
            package_info = {
                'name': package.name,
                'type': 'free' if package.monthly_price_yearly_subscription_in_cents == 0 else
                        'yearly_only' if package.monthly_price_cents is None else 'full',
                'yearly_subscription': package.monthly_price_yearly_subscription_in_cents
            }
            if package.monthly_price_cents is not None:
                package_info['monthly_subscription'] = package.monthly_price_cents
            
            result.append(package_info)

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error searching packages: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500