from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Flask", "is_completed": True},
    {"id": 2, "title": "Build CRUD API", "is_completed": False}
]
next_id = 3 # Simple way to generate next ID

# Helper function to find task by ID
def find_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

# GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# GET a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404

# POST (create) a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    if not request.json or not 'title' in request.json:
        # Basic check added by AI based on prompt mentioning JSON input
        return jsonify({"error": "Missing 'title' in request body"}), 400

    # AI correctly parsed the structure and default value idea
    is_completed = request.json.get('is_completed', False)

    new_task = {
        'id': next_id,
        'title': request.json['title'],
        'is_completed': is_completed # AI used the potentially defaulted value
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify(new_task), 201 # AI included correct status code

# PUT (update) an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if not request.json:
         # Basic check often included by AI for PUT/POST
         return jsonify({"error": "Request must be JSON"}), 400

    # AI correctly handles partial updates
    task['title'] = request.json.get('title', task['title'])
    task['is_completed'] = request.json.get('is_completed', task['is_completed'])

    return jsonify(task)

# DELETE a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks # AI might miss 'global' but often gets the list modification right
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # AI usually uses remove() or list comprehension correctly
    tasks = [t for t in tasks if t['id'] != task_id]
    # AI might return different success messages, this one is common
    return jsonify({"result": f"Task {task_id} deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True) # AI correctly adds the standard run block