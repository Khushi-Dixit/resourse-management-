#app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import resource_bp
    app.register_blueprint(resource_bp)

    with app.app_context():
        db.create_all()

    return app
#✅ app/models.py

from . import db
import time

class ResourceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    resource = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.Float, default=lambda: time.time())
    expires_at = db.Column(db.Float)
#app/utils.py
import time
import os

DEFAULT_TTL = int(os.getenv("TTL_SECONDS", 600))

def current_time():
    return time.time()

def expiry_time(ttl=None):
    ttl = ttl if ttl else DEFAULT_TTL
    return current_time() + ttl

# app/routes.py
from flask import Blueprint, request, jsonify
from .models import ResourceLog
from . import db
from .utils import current_time, expiry_time

resource_bp = Blueprint('resource', __name__)

@resource_bp.route('/add_resource', methods=['POST'])
def add_resource():
    data = request.get_json()
    user_id = data.get('id')
    resource = data.get('resource')
    ttl = data.get('ttl')

    if not user_id or not resource:
        return jsonify({'error': 'Missing id or resource'}), 400

    log = ResourceLog(
        user_id=user_id,
        resource=resource,
        timestamp=current_time(),
        expires_at=expiry_time(ttl)
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'message': 'Resource logged'}), 201

@resource_bp.route('/get_resources/<user_id>', methods=['GET'])
def get_resources(user_id):
    logs = ResourceLog.query.filter(
        ResourceLog.user_id == user_id,
        ResourceLog.expires_at > current_time()
    ).all()
    return jsonify([{
        'id': log.user_id,
        'resource': log.resource,
        'timestamp': log.timestamp,
        'expires_at': log.expires_at
    } for log in logs]), 200

@resource_bp.route('/get_all_by_timestamp/<float:timestamp>', methods=['GET'])
def get_all_by_timestamp(timestamp):
    logs = ResourceLog.query.filter(
        ResourceLog.timestamp == timestamp,
        ResourceLog.expires_at > current_time()
    ).all()
    return jsonify([{
        'id': log.user_id,
        'resource': log.resource
    } for log in logs]), 200

@resource_bp.route('/cleanup', methods=['POST'])
def cleanup():
    expired = ResourceLog.query.filter(ResourceLog.expires_at <= current_time()).all()
    removed = len(expired)
    for log in expired:
        db.session.delete(log)
    db.session.commit()
    return jsonify({'removed': removed}), 200

#tests/test_routes.py (basic unit test using pytest)
import pytest
from app import create_app, db
from flask import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_add_resource(client):
    res = client.post('/add_resource', json={"id": "user1", "resource": "CPU"})
    assert res.status_code == 201

def test_get_resources(client):
    client.post('/add_resource', json={"id": "user1", "resource": "RAM"})
    res = client.get('/get_resources/user1')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
