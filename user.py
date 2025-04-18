from flask import Blueprint, jsonify, request
from firebase import db

user_bp = Blueprint('user', __name__)

# Fetch tenant details
@user_bp.route('/tenant/<tenant_id>', methods=['GET'])
def get_tenant(tenant_id):
    try:
        tenant_ref = db.collection('tenants').document(tenant_id)
        tenant = tenant_ref.get()
        if tenant.exists:
            return jsonify(tenant.to_dict()), 200
        return jsonify({'error': 'Tenant not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update payment history
@user_bp.route('/tenant/<tenant_id>/payment', methods=['POST'])
def add_payment(tenant_id):
    try:
        data = request.json
        tenant_ref = db.collection('tenants').document(tenant_id)
        tenant_ref.update({
            'paymentHistory': firestore.ArrayUnion([data])
        })
        return jsonify({'message': 'Payment added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500