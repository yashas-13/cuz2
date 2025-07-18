from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from .. import db
from ..models import ApprovalRequest
from ..services.requests import (
    create_request,
    approve_request,
    deny_request,
    bulk_approve_requests,
    bulk_deny_requests,
    create_draft_request,
)
from ...utils.decorators import role_required

requests_bp = Blueprint('requests', __name__)

@requests_bp.route('/', methods=['GET'])
@role_required('Manufacturer', 'CFA')
def list_requests():
    status = request.args.get('status')
    requester_id = request.args.get('requester_id')
    product_id = request.args.get('product')
    start = request.args.get('start')
    end = request.args.get('end')
    query = ApprovalRequest.query
    if status:
        query = query.filter_by(status=status)
    if requester_id:
        query = query.filter_by(requester_id=int(requester_id))
    if product_id:
        query = query.filter_by(product_id=int(product_id))
    if start:
        query = query.filter(ApprovalRequest.created_at >= start)
    if end:
        query = query.filter(ApprovalRequest.created_at <= end)
    requests_list = query.all()
    return jsonify([
        {
            'id': r.id,
            'product_id': r.product_id,
            'action': r.action,
            'quantity': r.quantity,
            'location_id': r.location_id,
            'status': r.status
        } for r in requests_list
    ])

@requests_bp.route('/', methods=['POST'])
@role_required('CFA')
def new_request():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    action = data.get('action')
    quantity = data.get('quantity', 0)
    location_id = data.get('location_id', 0)
    if None in (product_id, action):
        return jsonify({'msg': 'missing fields'}), 400
    req_obj = create_request(get_jwt_identity(), product_id, action, quantity, location_id)
    return jsonify({'id': req_obj.id}), 201


@requests_bp.route('/draft', methods=['POST'])
@role_required('CFA')
def save_draft():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    action = data.get('action')
    quantity = data.get('quantity', 0)
    location_id = data.get('location_id', 0)
    req_obj = create_draft_request(get_jwt_identity(), product_id, action, quantity, location_id)
    return jsonify({'id': req_obj.id}), 201

@requests_bp.route('/<int:id>/approve', methods=['PUT'])
@role_required('Manufacturer')
def approve(id):
    req_obj = ApprovalRequest.query.get_or_404(id)
    approve_request(req_obj, get_jwt_identity())
    return jsonify({'msg': 'approved'})

@requests_bp.route('/<int:id>/deny', methods=['PUT'])
@role_required('Manufacturer')
def deny(id):
    req_obj = ApprovalRequest.query.get_or_404(id)
    deny_request(req_obj, get_jwt_identity())
    return jsonify({'msg': 'denied'})


@requests_bp.route('/bulk-approve', methods=['PUT'])
@role_required('Manufacturer')
def bulk_approve():
    data = request.get_json() or {}
    ids = data.get('ids', [])
    bulk_approve_requests(ids, get_jwt_identity())
    return jsonify({'approved': ids})


@requests_bp.route('/bulk-deny', methods=['PUT'])
@role_required('Manufacturer')
def bulk_deny():
    data = request.get_json() or {}
    ids = data.get('ids', [])
    bulk_deny_requests(ids, get_jwt_identity())
    return jsonify({'denied': ids})
