from .. import db
from ..models import Product


def create_product(name, description, price, manufacturer_id):
    product = Product(name=name, description=description, price=price, manufacturer_id=manufacturer_id)
    db.session.add(product)
    db.session.commit()
    return product


def bulk_create_products(data_list):
    """Create multiple products at once.

    Each item in ``data_list`` should be a dict with keys ``name``, ``description``,
    ``price`` and ``manufacturer_id``. The operation is executed in a single
    transaction so either all products are created or none.
    """
    products = [
        Product(name=item['name'],
                description=item.get('description', ''),
                price=item['price'],
                manufacturer_id=item['manufacturer_id'])
        for item in data_list
    ]
    db.session.add_all(products)
    db.session.commit()
    return products


def bulk_update_products(data_list):
    """Update multiple products.

    ``data_list`` is a list of dictionaries, each containing at least ``id`` and
    the fields to update. Missing fields are ignored.
    """
    updated = []
    for item in data_list:
        product = Product.query.get(item['id'])
        if not product:
            continue
        product.name = item.get('name', product.name)
        product.description = item.get('description', product.description)
        product.price = item.get('price', product.price)
        updated.append(product)
    db.session.commit()
    return updated
