import json
from backend.app import create_app, db
from backend.app.models import Role


def setup_app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Role(name='Manufacturer'))
        db.session.add(Role(name='CFA'))
        db.session.add(Role(name='Stockist'))
        db.session.commit()
    return app


def test_register_and_login():
    app = setup_app()
    client = app.test_client()
    resp = client.post('/auth/register', json={'username': 'user', 'email': 'u@example.com', 'password': 'pass', 'role': 'Manufacturer'})
    assert resp.status_code == 201
    resp = client.post('/auth/login', json={'username': 'user', 'password': 'pass'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'access_token' in data
