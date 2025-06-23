import json
from .. import db
from ..models import Order


def create_order(stockist_id, items):
    order = Order(stockist_id=stockist_id, items=json.dumps(items))
    db.session.add(order)
    db.session.commit()
    return order


def list_orders(user):
    if user.role.name == 'Manufacturer':
        return Order.query.all()
    return Order.query.filter_by(stockist_id=user.id).all()
