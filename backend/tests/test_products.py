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


def test_bulk_create_update():
    app = setup_app()
    client = app.test_client()
    with app.app_context():
        user = User.query.filter_by(username='manu').first()
        token = create_access_token(identity=str(user.id), additional_claims={'role': 'Manufacturer'})
    headers = {'Authorization': f'Bearer {token}'}
    bulk_data = [
        {'name': 'p1', 'price': 1, 'manufacturer_id': 1},
        {'name': 'p2', 'price': 2, 'manufacturer_id': 1}
    ]
    resp = client.post('/products/bulk', json=bulk_data, headers=headers)
    assert resp.status_code == 201
    ids = json.loads(resp.data)['created']
    assert len(ids) == 2
    update_data = [
        {'id': ids[0], 'price': 5},
        {'id': ids[1], 'name': 'p2-new'}
    ]
    resp = client.patch('/products/bulk', json=update_data, headers=headers)
    assert resp.status_code == 200
    resp = client.get('/products/', headers=headers)
    products = {p['id']: p for p in json.loads(resp.data)}
    assert products[ids[0]]['price'] == 5
    assert products[ids[1]]['name'] == 'p2-new'
