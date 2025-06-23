from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from .. import db
from ..models import User, Role

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role', 'Stockist')

    if not username or not email or not password:
        return jsonify({'msg': 'Missing required fields'}), 400

    role = Role.query.filter_by(name=role_name).first()
    if role is None:
        role = Role(name=role_name)
        db.session.add(role)
        db.session.commit()

    user = User(username=username, email=email,
                password_hash=User.generate_hash(password), role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'user created'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not User.verify_hash(password, user.password_hash):
        return jsonify({'msg': 'Bad credentials'}), 401

    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role.name})
    return jsonify(access_token=access_token)
