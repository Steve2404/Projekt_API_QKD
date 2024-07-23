from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class KeyMaterial(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    kme_id = db.Column(db.String(80), nullable=False)
    key_value = db.Column(db.Text, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)


class KeyRequest(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    master_sae_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slave_sae_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requested_key_count = db.Column(db.Integer, nullable=False)
    requested_key_size = db.Column(db.Integer, nullable=False)
    request_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)


class KeyDelivery(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    request_id = db.Column(db.String(36), db.ForeignKey('key_request.id'), nullable=False)
    key_id = db.Column(db.String(36), db.ForeignKey('key_material.id'), nullable=False)
    delivery_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
