'''✅ code.py (Flask App with Resource Management)
✅ This includes: resource logging, expiration, retrieval, and cleanup logic.'''

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///resources.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TTL from .env
TTL_SECONDS = int(os.getenv('TTL_SECONDS', 600))

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "expires_at": self.expires_at.isoformat()
        }

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/log', methods=['POST'])
def log_resource():
    data = request.json
    user_id = data.get('user_id')
    resource_data = data.get('data')
    expires_at = datetime.utcnow() + timedelta(seconds=TTL_SECONDS)

    new_resource = Resource(user_id=user_id, data=resource_data, expires_at=expires_at)
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Resource logged successfully"}), 201

@app.route('/resources/<user_id>', methods=['GET'])
def get_resources(user_id):
    cleanup_expired_resources()
    resources = Resource.query.filter_by(user_id=user_id).all()
    return jsonify([res.to_dict() for res in resources])

@app.route('/resources', methods=['GET'])
def get_all_resources():
    cleanup_expired_resources()
    resources = Resource.query.all()
    return jsonify([res.to_dict() for res in resources])

def cleanup_expired_resources():
    now = datetime.utcnow()
    expired = Resource.query.filter(Resource.expires_at <= now).all()
    for res in expired:
        db.session.delete(res)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)


#.env
DATABASE_URI=sqlite:///resources.db
TTL_SECONDS=600
FLASK_ENV=development
