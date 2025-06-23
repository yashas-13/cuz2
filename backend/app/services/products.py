from .. import db
from ..models import Product


def create_product(name, description, price, manufacturer_id):
    product = Product(name=name, description=description, price=price, manufacturer_id=manufacturer_id)
    db.session.add(product)
    db.session.commit()
    return product
