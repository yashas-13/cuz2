from flask import Blueprint, request, jsonify

from .. import db
from ..models import Product, User
from ..services.products import create_product
from ...utils.decorators import role_required

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
@role_required('Manufacturer', 'CFA', 'Stockist')
def list_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price} for p in products])

@products_bp.route('/', methods=['POST'])
@role_required('Manufacturer')
def add_product():
    data = request.get_json() or {}
    name = data.get('name')
    price = data.get('price')
    manufacturer_id = data.get('manufacturer_id')
    description = data.get('description', '')
    if not name or price is None or manufacturer_id is None:
        return jsonify({'msg': 'missing fields'}), 400
    product = create_product(name, description, price, manufacturer_id)
    return jsonify({'id': product.id}), 201

@products_bp.route('/<int:id>', methods=['GET'])
@role_required('Manufacturer', 'CFA', 'Stockist')
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price})

@products_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@role_required('Manufacturer')
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json() or {}
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    db.session.commit()
    return jsonify({'msg': 'updated'})

@products_bp.route('/<int:id>', methods=['DELETE'])
@role_required('Manufacturer')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'msg': 'deleted'})
