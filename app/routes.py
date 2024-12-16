# app/routes.py
from flask import Blueprint, request, jsonify
from app.models import db, Todo

todo_bp = Blueprint('todo_bp', __name__)

# Route to add a new To-Do task
@todo_bp.route('/todo', methods=['POST'])
def add_task():
    task_data = request.json
    task = task_data.get('task', '')

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    # Insert the new task into PostgreSQL
    new_task = Todo(task=task)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'task': new_task.task}), 201


# Route to display all To-Do tasks
@todo_bp.route('/todos', methods=['GET'])
def get_tasks():
    tasks = Todo.query.all()
    task_list = [{'id': task.id, 'task': task.task} for task in tasks]
    return jsonify(task_list)


# Route to edit a particular To-Do task
@todo_bp.route('/todo/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task_data = request.json
    task = task_data.get('task', '')

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    # Update the task in PostgreSQL
    existing_task = Todo.query.get(task_id)
    if not existing_task:
        return jsonify({'error': 'Task not found'}), 404

    existing_task.task = task
    db.session.commit()
    return jsonify({'id': existing_task.id, 'task': existing_task.task})


# Route to delete a particular To-Do task
@todo_bp.route('/todo/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Delete the task from PostgreSQL
    task_to_delete = Todo.query.get(task_id)
    if not task_to_delete:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task_to_delete)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})


# Route to delete all To-Do tasks
@todo_bp.route('/todos', methods=['DELETE'])
def delete_all_tasks():
    # Delete all tasks from PostgreSQL
    deleted_count = db.session.query(Todo).delete()
    db.session.commit()
    return jsonify({'message': f'{deleted_count} tasks deleted'}), 200
