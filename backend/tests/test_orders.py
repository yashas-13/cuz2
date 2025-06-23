import json
from flask_jwt_extended import create_access_token
from backend.app import create_app, db
from backend.app.models import Role, User


def setup_app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.drop_all()
        db.create_all()
        stock_role = Role(name='Stockist')
        man_role = Role(name='Manufacturer')
        db.session.add_all([stock_role, man_role, Role(name='CFA')])
        db.session.commit()
        stock = User(username='st', email='s@example.com', password_hash=User.generate_hash('pass'), role=stock_role)
        db.session.add(stock)
        db.session.commit()
    return app


def test_order_creation():
    app = setup_app()
    client = app.test_client()
    with app.app_context():
        stock = User.query.filter_by(username='st').first()
        token = create_access_token(identity=str(stock.id), additional_claims={'role': 'Stockist'})
    headers = {'Authorization': f'Bearer {token}'}
    resp = client.post('/orders/', json={'items': [{'product_id':1,'qty':2}]}, headers=headers)
    assert resp.status_code == 201
    order_id = json.loads(resp.data)['id']
    resp = client.get('/orders/', headers=headers)
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert any(o['id'] == order_id for o in data)
