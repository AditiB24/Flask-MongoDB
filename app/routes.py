from flask import Blueprint, request, jsonify
from app.models import create_todo, get_todos, update_task, delete_task, delete_all_tasks

# Blueprint for To-Do routes
todo_bp = Blueprint('todo_bp', __name__)

# Route to add a new To-Do task
@todo_bp.route('/todo', methods=['POST'])
def add_task():
    task_data = request.json
    task = task_data.get('task', '')  # Get the 'task' from the request JSON

    if not task:  # Check if task is empty or not provided
        return jsonify({'error': 'Task is required'}), 400

    # Insert the new task into PostgreSQL using psycopg2
    create_todo(task, False)  # 'False' for completed as default
    return jsonify({'task': task, 'completed': False}), 201  # Return the added task details


# Route to display all To-Do tasks
@todo_bp.route('/todos', methods=['GET'])
def get_tasks():
    tasks = get_todos()  # Get all tasks from PostgreSQL
    task_list = [{'id': task[0], 'task': task[1], 'completed': task[2]} for task in tasks]  # Format the data
    return jsonify(task_list)  # Return list of tasks


# Route to edit a particular To-Do task
@todo_bp.route('/todo/<int:task_id>', methods=['PUT'])
def update_task_route(task_id):
    task_data = request.json
    task = task_data.get('task', '')  # Get the updated task description

    if not task:  # If no task is provided
        return jsonify({'error': 'Task is required'}), 400

    # Update the task in PostgreSQL
    update_task(task_id, task)
    return jsonify({'id': task_id, 'task': task})  # Return updated task


# Route to delete a particular To-Do task
@todo_bp.route('/todo/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    # Delete the task from PostgreSQL
    delete_task(task_id)
    return jsonify({'message': 'Task deleted successfully'})  # Success message


# Route to delete all To-Do tasks
@todo_bp.route('/todos', methods=['DELETE'])
def delete_all_tasks_route():
    # Delete all tasks from PostgreSQL
    delete_all_tasks()
    return jsonify({'message': 'All tasks deleted successfully'})  # Success message
