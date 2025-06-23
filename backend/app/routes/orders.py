import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from .. import db
from ..models import User
from ..services.orders import create_order, list_orders
from ...utils.decorators import role_required


orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/', methods=['GET'])
@role_required('Manufacturer', 'Stockist')
def get_orders():
    user = User.query.get(get_jwt_identity())
    orders = list_orders(user)
    return jsonify([
        {'id': o.id, 'items': json.loads(o.items), 'status': o.status}
        for o in orders
    ])


@orders_bp.route('/', methods=['POST'])
@role_required('Stockist')
def place_order():
    data = request.get_json() or {}
    items = data.get('items', [])
    order = create_order(get_jwt_identity(), items)
    return jsonify({'id': order.id}), 201
