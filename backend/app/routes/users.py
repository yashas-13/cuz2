from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from .. import db
from ..models import User
from ...utils.decorators import role_required

users_bp = Blueprint('users', __name__)


@users_bp.route('/me', methods=['GET'])
@role_required('Stockist')
def get_profile():
    user = User.query.get(get_jwt_identity())
    return jsonify({'username': user.username, 'email': user.email})


@users_bp.route('/me', methods=['PUT'])
@role_required('Stockist')
def update_profile():
    user = User.query.get(get_jwt_identity())
    data = request.get_json() or {}
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data and 'current_password' in data and User.verify_hash(data['current_password'], user.password_hash):
        user.password_hash = User.generate_hash(data['password'])
    db.session.commit()
    return jsonify({'msg': 'updated'})
