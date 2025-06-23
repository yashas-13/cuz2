import json
from flask_jwt_extended import create_access_token
from backend.app import create_app, db
from backend.app.models import Role, User, Inventory

def setup_app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.drop_all()
        db.create_all()
        man_role = Role(name='Manufacturer')
        stock_role = Role(name='Stockist')
        db.session.add_all([man_role, Role(name='CFA'), stock_role])
        db.session.commit()
        man = User(username='man', email='m@example.com', password_hash=User.generate_hash('pass'), role=man_role)
        stock = User(username='st', email='s@example.com', password_hash=User.generate_hash('pass'), role=stock_role)
        db.session.add_all([man, stock])
        db.session.commit()
        inv = Inventory(product_id=1, location_id=1, quantity=10)
        db.session.add(inv)
        db.session.commit()
    return app


def test_inventory_get_for_stockist():
    app = setup_app()
    client = app.test_client()
    with app.app_context():
        stock = User.query.filter_by(username='st').first()
        token = create_access_token(identity=str(stock.id), additional_claims={'role': 'Stockist'})
    resp = client.get('/inventory/', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data and data[0]['quantity'] == 10
