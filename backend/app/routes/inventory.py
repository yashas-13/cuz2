from flask import Blueprint, request, jsonify

from .. import db
from ..models import Inventory
from ..services.inventory import adjust_inventory
from ...utils.decorators import role_required

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/', methods=['GET'])
@role_required('Manufacturer', 'CFA', 'Stockist')
def list_inventory():
    items = Inventory.query.all()
    return jsonify([{'id': i.id, 'product_id': i.product_id, 'location_id': i.location_id, 'quantity': i.quantity} for i in items])

@inventory_bp.route('/<int:id>', methods=['GET'])
@role_required('Manufacturer', 'CFA', 'Stockist')
def get_inventory(id):
    inv = Inventory.query.get_or_404(id)
    return jsonify({'id': inv.id, 'product_id': inv.product_id, 'location_id': inv.location_id, 'quantity': inv.quantity})

@inventory_bp.route('/', methods=['POST'])
@role_required('Manufacturer')
def set_inventory():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    location_id = data.get('location_id')
    quantity = data.get('quantity')
    if None in (product_id, location_id, quantity):
        return jsonify({'msg': 'missing fields'}), 400
    inv = adjust_inventory(product_id, location_id, quantity)
    return jsonify({'id': inv.id}), 201


@inventory_bp.route('/<int:id>', methods=['PATCH'])
@role_required('Manufacturer')
def update_inventory(id):
    inv = Inventory.query.get_or_404(id)
    data = request.get_json() or {}
    quantity = data.get('quantity', inv.quantity)
    inv.quantity = quantity
    db.session.commit()
    return jsonify({'msg': 'updated'})
