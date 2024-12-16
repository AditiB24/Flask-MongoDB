from flask import Blueprint, request, jsonify
from app.models import create_todo, get_todos, update_task, delete_task, delete_all_tasks

todo_bp = Blueprint('todo_bp', __name__)

# Route to add a new To-Do task
@todo_bp.route('/todo', methods=['POST'])
def add_task():
    task_data = request.json
    task = task_data.get('task', '')

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    # Insert the new task into PostgreSQL using psycopg2
    create_todo(task, False)  # 'False' for completed as default
    return jsonify({'task': task, 'completed': False}), 201

# Route to display all To-Do tasks
@todo_bp.route('/todos', methods=['GET'])
def get_tasks():
    tasks = get_todos()
    task_list = [{'id': task[0], 'task': task[1], 'completed': task[2]} for task in tasks]
    return jsonify(task_list)

# Route to edit a particular To-Do task
@todo_bp.route('/todo/<int:task_id>', methods=['PUT'])
def update_task_route(task_id):
    task_data = request.json
    task = task_data.get('task', '')

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    # Update the task in PostgreSQL
    update_task(task_id, task)
    return jsonify({'id': task_id, 'task': task})

# Route to delete a particular To-Do task
@todo_bp.route('/todo/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    # Delete the task from PostgreSQL
    delete_task(task_id)
    return jsonify({'message': 'Task deleted successfully'})

# Route to delete all To-Do tasks
@todo_bp.route('/todos', methods=['DELETE'])
def delete_all_tasks_route():
    # Delete all tasks from PostgreSQL
    delete_all_tasks()
    return jsonify({'message': 'All tasks deleted successfully'})
