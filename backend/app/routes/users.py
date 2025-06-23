from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from .. import db
from ..models import User, Role
from ...utils.decorators import role_required

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['POST'])
@role_required('Manufacturer')
def create_user():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')

    if not username or not email or not password or role_name not in ['CFA', 'Stockist']:
        return jsonify({'msg': 'invalid data'}), 400

    role = Role.query.filter_by(name=role_name).first()
    if role is None:
        role = Role(name=role_name)
        db.session.add(role)
        db.session.commit()

    creator_id = get_jwt_identity()
    user = User(username=username, email=email,
                password_hash=User.generate_hash(password), role=role,
                created_by_id=creator_id)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201


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
