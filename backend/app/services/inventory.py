from .. import db
from ..models import Inventory


def adjust_inventory(product_id, location_id, quantity):
    inv = Inventory.query.filter_by(product_id=product_id, location_id=location_id).first()
    if not inv:
        inv = Inventory(product_id=product_id, location_id=location_id, quantity=0)
        db.session.add(inv)
    inv.quantity = quantity
    db.session.commit()
    return inv
