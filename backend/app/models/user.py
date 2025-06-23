from .. import db
from passlib.hash import pbkdf2_sha256 as sha256

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_users = db.relationship('User', backref=db.backref('creator', remote_side=[id]), lazy=True)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)
