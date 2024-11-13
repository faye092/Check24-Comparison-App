from flask import Blueprint, jsonify
from models import StreamingPackage

packages_blueprint = Blueprint('packages', __name__)

@packages_blueprint.route('/', methods=['GET'])
def get_packages():
    packages = StreamingPackage.query.all()
    return jsonify([{
        'id': package.id,
        'name': package.name,
        'monthly_price_cents': package.monthly_price_cents,
        'monthly_price_yearly_subscription_in_cents': package.monthly_price_yearly_subscription_in_cents
    } for package in packages])
