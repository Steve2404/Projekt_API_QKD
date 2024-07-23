from datetime import timezone
from flask import Blueprint, request, jsonify
from models import User, KeyMaterial, KeyRequest, KeyDelivery, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import uuid

keys_bp = Blueprint('keys', __name__)


@keys_bp.route('/keys/<string:sae_id>/status', methods=['GET'])
@jwt_required()
def get_key_status(sae_id):
    if keys := KeyMaterial.query.filter_by(status='active').all():
        return jsonify([key.id for key in keys]), 200
    else:
        return jsonify({'message': 'No active keys available'}), 404


@keys_bp.route('/keys/<string:sae_id>/enc_keys', methods=['POST'])
@jwt_required()
def get_key(sae_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    key_count = data.get('key_count')
    key_size = data.get('key_size')

    # Generate Key IDs and Key Materials
    keys = []
    for _ in range(key_count):
        key_id = str(uuid.uuid4())
        key_value = str(uuid.uuid4())  # This should be a real key value generated securely
        key_material = KeyMaterial(
            id=key_id,
            kme_id=current_user,
            key_value=key_value,
            creation_time=datetime.now(timezone.utc),
            status='active',
        )
        db.session.add(key_material)
        keys.append(key_id)

    db.session.commit()

    return jsonify({'key_ids': keys}), 201


@keys_bp.route('/keys/<string:sae_id>/dec_keys', methods=['POST'])
@jwt_required()
def get_key_with_id(sae_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    key_id = data.get('key_id')
    if key_material := KeyMaterial.query.filter_by(
        id=key_id, status='active'
    ).first():
        return jsonify({'key_value': key_material.key_value}), 200
    else:
        return jsonify({'message': 'Key not found or inactive'}), 404
