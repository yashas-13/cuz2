from .. import db
from ..models import ApprovalRequest, Inventory


def create_request(requester_id, product_id, action, quantity, location_id):
    approval = ApprovalRequest(requester_id=int(requester_id),
                               product_id=product_id,
                               action=action,
                               quantity=quantity,
                               location_id=location_id,
                               status='pending')
    db.session.add(approval)
    db.session.commit()
    return approval


def approve_request(request_obj, approver_id):
    request_obj.status = 'approved'
    request_obj.approver_id = approver_id
    inv = Inventory.query.filter_by(product_id=request_obj.product_id,
                                    location_id=request_obj.location_id).first()
    if not inv:
        inv = Inventory(product_id=request_obj.product_id,
                         location_id=request_obj.location_id,
                         quantity=0)
        db.session.add(inv)
    if request_obj.action == 'add':
        inv.quantity += request_obj.quantity
    elif request_obj.action == 'remove':
        inv.quantity = max(0, inv.quantity - request_obj.quantity)
    db.session.commit()


def deny_request(request_obj, approver_id):
    request_obj.status = 'denied'
    request_obj.approver_id = approver_id
    db.session.commit()
