# ---- Save this code as app.py ----

from flask import Flask, request, jsonify, abort, render_template
from flask_cors import CORS # Import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# In-memory storage for items (list of dictionaries)
# Start with some example data
items = [
    {'id': 1, 'name': 'Learn Flask'},
    {'id': 2, 'name': 'Build CRUD App'}
]
# Counter for generating the next unique ID
next_id = 3 # Start after the initial items

# --- Helper Function ---
def find_item_or_404(item_id):
    """Searches for an item by ID. Returns the item or aborts with 404."""
    try:
        item_id_int = int(item_id) # Ensure ID is integer for comparison
        item = next((item for item in items if item['id'] == item_id_int), None)
        if item is None:
            abort(404, description=f"Item with ID {item_id_int} not found")
        return item
    except ValueError:
        abort(400, description=f"Invalid item ID format: {item_id}")


# --- API Endpoints (CRUD Operations) ---

# CREATE: Add a new item
@app.route('/api/items', methods=['POST'])
def create_item():
    global next_id
    if not request.json or not 'name' in request.json or not request.json['name'].strip():
        abort(400, description="Request must be JSON and contain a non-empty 'name' field.")
    new_item = {
        'id': next_id,
        'name': request.json['name'].strip()
    }
    items.append(new_item)
    next_id += 1
    return jsonify(new_item), 201

# READ: Get all items
@app.route('/api/items', methods=['GET'])
def get_all_items():
    return jsonify(items)

# READ: Get a specific item by ID
@app.route('/api/items/<item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item_or_404(item_id)
    return jsonify(item)

# UPDATE: Modify an existing item by ID
@app.route('/api/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    item = find_item_or_404(item_id)
    if not request.json or not 'name' in request.json or not request.json['name'].strip():
         abort(400, description="Request must be JSON and contain a non-empty 'name' field.")
    item['name'] = request.json['name'].strip()
    return jsonify(item)

# DELETE: Remove an item by ID
@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item_to_delete = find_item_or_404(item_id) # Ensures item exists before filtering
    items = [item for item in items if item['id'] != item_to_delete['id']]
    return jsonify({'result': True, 'message': f'Item with ID {item_to_delete["id"]} deleted successfully'})

# --- Route to Serve the Frontend ---
@app.route('/')
def index():
    # Renders the index.html file from the 'templates' folder
    return render_template('index.html')

# --- Run the Flask Development Server ---
if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible on your network, not just localhost
    # port=5000 is the default Flask port
    app.run(host='0.0.0.0', port=5000, debug=True)