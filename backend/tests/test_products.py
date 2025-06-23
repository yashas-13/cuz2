import json
from flask_jwt_extended import create_access_token
from backend.app import create_app, db
from backend.app.models import Role, User, Product


def setup_app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.drop_all()
        db.create_all()
        manufacturer_role = Role(name='Manufacturer')
        db.session.add(manufacturer_role)
        db.session.add(Role(name='CFA'))
        db.session.add(Role(name='Stockist'))
        db.session.commit()
        user = User(username='manu', email='m@example.com', password_hash=User.generate_hash('pass'), role=manufacturer_role)
        db.session.add(user)
        db.session.commit()
    return app


def test_product_crud():
    app = setup_app()
    client = app.test_client()
    with app.app_context():
        user = User.query.filter_by(username='manu').first()
        token = create_access_token(identity=str(user.id), additional_claims={'role': 'Manufacturer'})
    headers = {'Authorization': f'Bearer {token}'}
    resp = client.post('/products/', json={'name': 'prod', 'price': 1.0, 'manufacturer_id': 1}, headers=headers)
    assert resp.status_code == 201
    prod_id = json.loads(resp.data)['id']
    resp = client.get('/products/', headers=headers)
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert any(p['id'] == prod_id for p in data)
