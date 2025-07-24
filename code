from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# In-memory storage for resource logs
resource_logs = []

# Default TTL for resource logs in seconds
DEFAULT_TTL = 600  # 10 minutes

@app.route('/add_resource', methods=['POST'])
def add_resource():
    data = request.get_json()
    user_id = data.get('id')
    resource = data.get('resource')
    ttl = data.get('ttl', DEFAULT_TTL)

    if not user_id or not resource:
        return jsonify({'error': 'Missing id or resource'}), 400

    timestamp = time.time()
    expires_at = timestamp + ttl

    log_entry = {
        'id': user_id,
        'resource': resource,
        'timestamp': timestamp,
        'expires_at': expires_at
    }
    resource_logs.append(log_entry)

    return jsonify({
        'message': 'Resource logged',
        'timestamp': timestamp
    }), 201

@app.route('/get_resources/<user_id>', methods=['GET'])
def get_resources(user_id):
    current_time = time.time()
    valid_logs = [log for log in resource_logs
                  if log['id'] == user_id and log['expires_at'] > current_time]
    
    return jsonify({'resources': valid_logs}), 200

@app.route('/get_all_by_timestamp/<float:timestamp>', methods=['GET'])
def get_all_by_timestamp(timestamp):
    current_time = time.time()
    logs = [log for log in resource_logs
            if log['timestamp'] == timestamp and log['expires_at'] > current_time]
    
    return jsonify({'logs': logs}), 200

@app.route('/cleanup', methods=['POST'])
def cleanup_expired_logs():
    current_time = time.time()
    before = len(resource_logs)
    resource_logs[:] = [log for log in resource_logs if log['expires_at'] > current_time]
    after = len(resource_logs)
    removed = before - after
    return jsonify({'removed': removed, 'remaining': after}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Resource Management API is running.",
        "endpoints": [
            "/add_resource [POST]",
            "/get_resources/<id> [GET]",
            "/get_all_by_timestamp/<timestamp> [GET]",
            "/cleanup [POST]"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
