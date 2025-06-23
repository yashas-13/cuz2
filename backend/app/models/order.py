from datetime import datetime
from .. import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stockist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.Column(db.Text, nullable=False)  # JSON string
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
