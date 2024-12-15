# app/routes.py
from flask import Blueprint, request, jsonify
from app.models import mongo

todo_bp = Blueprint('todo_bp', __name__)

# Route to add a new To-Do task
@todo_bp.route('/todo', methods=['POST'])
def add_task():
    task_data = request.json
    task = task_data.get('task', '')

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    # Insert the new task into MongoDB
    task_id = mongo.db.tasks.insert_one({'task': task}).inserted_id
    return jsonify({'id': str(task_id), 'task': task}), 201


# Route to display all To-Do tasks
@todo_bp.route('/todos', methods=['GET'])
def get_tasks():
    tasks = mongo.db.tasks.find()
    task_list = [{'id': str(task['_id']), 'task': task['task']} for task in tasks]
    return jsonify(task_list)


# Route to edit a particular To-Do task
@todo_bp.route('/todo/<task_id>', methods=['PUT'])
def update_task(task_id):
    task_data = request.json
    task = task_data.get('task', '')

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    # Update the task in MongoDB
    result = mongo.db.tasks.update_one({'_id': task_id}, {'$set': {'task': task}})

    if result.matched_count == 0:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'id': task_id, 'task': task})


# Route to delete a particular To-Do task
@todo_bp.route('/todo/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Delete the task from MongoDB
    result = mongo.db.tasks.delete_one({'_id': task_id})

    if result.deleted_count == 0:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task deleted successfully'})


# Route to delete all To-Do tasks
@todo_bp.route('/todos', methods=['DELETE'])
def delete_all_tasks():
    # Delete all tasks from MongoDB
    result = mongo.db.tasks.delete_many({})
    return jsonify({'message': f'{result.deleted_count} tasks deleted'}), 200
