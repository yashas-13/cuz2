from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager



db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class=None):
    app = Flask(__name__)
    if config_class is None:
        from ..config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.products import products_bp
    from .routes.inventory import inventory_bp
    from .routes.requests import requests_bp
    from .routes.orders import orders_bp
    from .routes.users import users_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(requests_bp, url_prefix='/requests')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(users_bp, url_prefix='/users')

    with app.app_context():
        db.create_all()

    return app
