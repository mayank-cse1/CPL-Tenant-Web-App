from flask import Blueprint, jsonify, request
from firebase import db

admin_bp = Blueprint('admin', __name__)

# Fetch blocks
@admin_bp.route('/blocks', methods=['GET'])
def get_blocks():
    try:
        blocks_ref = db.collection('blocks')
        blocks = [doc.to_dict() for doc in blocks_ref.stream()]
        return jsonify(blocks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Fetch flats for a block
@admin_bp.route('/flats/<block_id>', methods=['GET'])
def get_flats(block_id):
    try:
        flats_ref = db.collection('flats').where('blockId', '==', block_id)
        flats = [doc.to_dict() for doc in flats_ref.stream()]
        return jsonify(flats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500