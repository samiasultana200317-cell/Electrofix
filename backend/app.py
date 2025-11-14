from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify([{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}])

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    # Process the order
    return jsonify({"status": "success", "order_id": 123})

# Serve static files (for your frontend)
@app.route('/')
def serve_index():
    return send_from_directory('../../', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../../', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)