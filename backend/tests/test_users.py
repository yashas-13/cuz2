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
        db.session.add_all([stock_role, Role(name='Manufacturer'), Role(name='CFA')])
        db.session.commit()
        user = User(username='st', email='s@example.com', password_hash=User.generate_hash('pass'), role=stock_role)
        db.session.add(user)
        db.session.commit()
    return app


def test_profile_update():
    app = setup_app()
    client = app.test_client()
    with app.app_context():
        user = User.query.filter_by(username='st').first()
        token = create_access_token(identity=str(user.id), additional_claims={'role': 'Stockist'})
    headers = {'Authorization': f'Bearer {token}'}
    resp = client.put('/users/me', json={'username': 'new'}, headers=headers)
    assert resp.status_code == 200
    resp = client.get('/users/me', headers=headers)
    data = json.loads(resp.data)
    assert data['username'] == 'new'
