from .. import db
from ..models import ApprovalRequest, Inventory


def create_request(requester_id, product_id, action, quantity, location_id):
    approval = ApprovalRequest(requester_id=int(requester_id),
                               product_id=product_id,
                               action=action,
                               status='pending')
    db.session.add(approval)
    db.session.commit()
    return approval


def approve_request(request_obj, approver_id):
    request_obj.status = 'approved'
    request_obj.approver_id = approver_id
    db.session.commit()
    # For demo: no inventory logic


def deny_request(request_obj, approver_id):
    request_obj.status = 'denied'
    request_obj.approver_id = approver_id
    db.session.commit()
