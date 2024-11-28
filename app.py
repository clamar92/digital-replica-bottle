from flask import Flask, request, jsonify
from db import get_db

app = Flask(__name__)
db = get_db()

# Endpoint for initializing the bottle
@app.route('/initialize', methods=['POST'])
def initialize_bottle():
    """Initialize the bottle with immutable data"""
    data = request.json
    required_fields = ["id", "type", "profile", "metadata"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if a bottle with the same ID already exists
    if db.bottles.find_one({"id": data["id"]}):  # Now checks by ID
        return jsonify({"error": f"Bottle with ID {data['id']} already initialized"}), 409

    # Insert the immutable data
    db.bottles.insert_one(data)
    return jsonify({"message": f"Bottle with ID {data['id']} initialized successfully"}), 201


# Endpoint for updating mutable data
@app.route('/update', methods=['POST'])
def update_bottle():
    """Update mutable fields for the bottle"""
    data = request.json
    mutable_fields = ["status", "room_id", "optimal_temperature", "measurements", "properties", "relations"]

    updates = {key: data[key] for key in data if key in mutable_fields}
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400

    result = db.bottles.update_one({}, {"$set": updates})  # Update the first (and only) bottle
    if result.matched_count == 0:
        return jsonify({"error": "Bottle not found"}), 404

    return jsonify({"message": "Bottle updated successfully"}), 200

# Endpoint for retrieving bottle data
@app.route('/bottle', methods=['GET'])
def get_bottle():
    """Retrieve the bottle data"""
    bottle = db.bottles.find_one()
    if not bottle:
        return jsonify({"error": "Bottle not initialized"}), 404

    bottle["_id"] = str(bottle["_id"])  # Convert MongoDB ObjectId to string
    return jsonify(bottle)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
