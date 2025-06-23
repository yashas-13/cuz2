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
        man_role = Role(name='Manufacturer')
        cfa_role = Role(name='CFA')
        db.session.add_all([man_role, cfa_role, Role(name='Stockist')])
        db.session.commit()
        man = User(username='man', email='man@example.com', password_hash=User.generate_hash('pass'), role=man_role)
        cfa = User(username='cfa', email='cfa@example.com', password_hash=User.generate_hash('pass'), role=cfa_role)
        db.session.add_all([man, cfa])
        db.session.commit()
    return app


def test_request_approval():
    app = setup_app()
    client = app.test_client()
    with app.app_context():
        cfa = User.query.filter_by(username='cfa').first()
        man = User.query.filter_by(username='man').first()
        cfa_token = create_access_token(identity=str(cfa.id), additional_claims={'role': 'CFA'})
        man_token = create_access_token(identity=str(man.id), additional_claims={'role': 'Manufacturer'})
    resp = client.post('/requests/', json={'product_id':1,'action':'add','quantity':5,'location_id':1}, headers={'Authorization': f'Bearer {cfa_token}'})
    assert resp.status_code == 201
    req_id = json.loads(resp.data)['id']
    resp = client.put(f'/requests/{req_id}/approve', headers={'Authorization': f'Bearer {man_token}'})
    assert resp.status_code == 200
    resp = client.get('/inventory/', headers={'Authorization': f'Bearer {cfa_token}'})
    data = json.loads(resp.data)
    assert any(i['product_id']==1 and i['quantity']==5 for i in data)


def test_bulk_approval():
    app = setup_app()
    client = app.test_client()
    with app.app_context():
        cfa = User.query.filter_by(username='cfa').first()
        man = User.query.filter_by(username='man').first()
        cfa_token = create_access_token(identity=str(cfa.id), additional_claims={'role': 'CFA'})
        man_token = create_access_token(identity=str(man.id), additional_claims={'role': 'Manufacturer'})
    headers_cfa = {'Authorization': f'Bearer {cfa_token}'}
    ids = []
    for _ in range(2):
        resp = client.post('/requests/', json={'product_id':1,'action':'add','quantity':2,'location_id':1}, headers=headers_cfa)
        ids.append(json.loads(resp.data)['id'])
    resp = client.put('/requests/bulk-approve', json={'ids': ids}, headers={'Authorization': f'Bearer {man_token}'})
    assert resp.status_code == 200
    resp = client.get('/inventory/', headers=headers_cfa)
    data = json.loads(resp.data)
    assert any(i['product_id']==1 and i['quantity']==4 for i in data)
