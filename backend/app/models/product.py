from .. import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    inventories = db.relationship('Inventory', backref='product', lazy=True)
