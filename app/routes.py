from flask import Blueprint, request, render_template, jsonify
from app.models import create_todo, get_todos

todo_bp = Blueprint('todo_bp', __name__)

# Route to Home (Display Tasks)
@todo_bp.route('/home', methods=['GET'])
def home():
    tasks = get_todos()  # Fetch tasks from the database
    task_list = [{'id': task[0], 'name': task[1], 'checked': task[2]} for task in tasks]
    return render_template('index.html', items=task_list)

# Route to Add a Task
@todo_bp.route('/home', methods=['POST'])
def add_task():
    task_name = request.form.get('todo_name')  # Get task name from form data

    if not task_name:
        return jsonify({"error": "Task name is required"}), 400  # Error if task name is empty

    # Insert the new task into the database (completed=False by default)
    create_todo(task_name, False)

    # Fetch the updated task list after inserting the new task
    tasks = get_todos()
    task_list = [{'id': task[0], 'name': task[1], 'checked': task[2]} for task in tasks]

    # Return the updated task list as JSON
    return jsonify({"tasks": task_list})
