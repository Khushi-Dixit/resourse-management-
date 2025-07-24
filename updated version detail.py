"""
Resource Management API

A Flask backend to log user-specific resources with TTL-based expiration,
persistent storage (SQLite), environment configuration, Docker support,
and basic unit testing—all contained in one file for easy setup.
"""

import os
import time
import sqlite3
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# -----------------------
# Configuration via .env
# -----------------------
load_dotenv()
TTL_SECONDS = int(os.getenv("TTL_SECONDS", 600))
DATABASE_URI = os.getenv("DATABASE_URI", "resources.db")
FLASK_ENV = os.getenv("FLASK_ENV", "development")

# -----------------------
# Flask App Setup
# -----------------------
app = Flask(__name__)

# -----------------------
# Database Initialization
# -----------------------
def init_db():
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resource_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            resource TEXT NOT NULL,
            timestamp REAL NOT NULL,
            expires_at REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# -----------------------
# Utility Functions
# -----------------------
def current_time():
    return time.time()

def expiry_time(ttl=None):
    return current_time() + (ttl if ttl else TTL_SECONDS)

def is_expired(entry):
    return current_time() > entry["expires_at"]

# -----------------------
# API Endpoints
# -----------------------

@app.route('/')
def index():
    return jsonify({
        "message": "Resource Management API is running.",
        "endpoints": [
            "/add_resource [POST]",
            "/get_resources/<user_id> [GET]",
            "/get_by_timestamp/<timestamp> [GET]",
            "/cleanup [POST]"
        ]
    })

@app.route('/add_resource', methods=['POST'])
def add_resource():
    data = request.get_json()
    uid = data.get('id')
    res = data.get('resource')
    ttl = data.get('ttl')

    if not uid or not res:
        return jsonify({'error': "Missing 'id' or 'resource'"}), 400

    ts = current_time()
    exp = expiry_time(ttl)

    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO resource_log (user_id, resource, timestamp, expires_at) VALUES (?, ?, ?, ?)
    ''', (uid, res, ts, exp))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Resource logged', 'timestamp': ts}), 201

@app.route('/get_resources/<user_id>', methods=['GET'])
def get_resources(user_id):
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, resource, timestamp, expires_at
        FROM resource_log
        WHERE user_id = ? AND expires_at > ?
    ''', (user_id, current_time()))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([
        {'id': uid, 'resource': res, 'timestamp': ts, 'expires_at': exp}
        for uid, res, ts, exp in rows
    ]), 200

@app.route('/get_by_timestamp/<float:timestamp>', methods=['GET'])
def get_by_timestamp(timestamp):
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, resource, timestamp
        FROM resource_log
        WHERE timestamp = ? AND expires_at > ?
    ''', (timestamp, current_time()))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([
        {'id': uid, 'resource': res, 'timestamp': ts}
        for uid, res, ts in rows
    ]), 200

@app.route('/cleanup', methods=['POST'])
def cleanup():
    conn = sqlite3.connect(DATABASE_URI)
    cursor = conn.cursor()
    now = current_time()
    cursor.execute('DELETE FROM resource_log WHERE expires_at <= ?', (now,))
    removed = conn.total_changes
    conn.commit()
    conn.close()
    return jsonify({'removed': removed}), 200

# -----------------------
# Unit Tests
# -----------------------
import unittest

class APITestCase(unittest.TestCase):
    def setUp(self):
        init_db()
        self.app = app.test_client()
        self.app.testing = True

    def test_add_and_get(self):
        r = self.app.post('/add_resource', json={'id':'user1','resource':'CPU'})
        self.assertEqual(r.status_code, 201)
        r2 = self.app.get('/get_resources/user1')
        data = r2.get_json()
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) >= 1)

    def test_cleanup(self):
        self.app.post('/add_resource', json={'id':'user2','resource':'Disk','ttl':1})
        time.sleep(2)
        r = self.app.post('/cleanup')
        data = r.get_json()
        self.assertTrue(data['removed'] >= 1)

if __name__ == '__main__':
    if FLASK_ENV == 'development':
        app.run(debug=True)
    else:
        unittest.main()



'''

🔧 Updated Folder Structure:

resource-management-api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── tests/
│   └── test_routes.py
├── .env
├── requirements.txt
├── Dockerfile
├── README.md
└── run.py

# .env
TTL_SECONDS=600
DATABASE_URI=sqlite:///resources.db
FLASK_ENV=development

#requirements.txt
Flask==3.0.3
python-dotenv==1.0.1
Flask-SQLAlchemy==3.1.1'''
