from flask import Blueprint, request, jsonify, render_template
from app.models import create_todo, get_todos, update_task, delete_task, delete_all_tasks

todo_bp = Blueprint('todo_bp', __name__)

# Home Route to Display the Index Page with the List of Tasks
@todo_bp.route('/home', methods=['GET'])
def home():
    # Fetch all tasks from the database
    tasks = get_todos()
    task_list = [{'id': task[0], 'name': task[1], 'checked': task[2]} for task in tasks]
    return render_template('index.html', items=task_list)

# Route to Add a New To-Do Task
@todo_bp.route('/home', methods=['POST'])
def add_task():
    task_name = request.form.get('todo_name')
    
    if not task_name:
        return jsonify({"error": "Task name is required"}), 400
    
    # Insert the new task into PostgreSQL (or MongoDB)
    create_todo(task_name, False)  # 'False' for completed as default
    
    # Fetch all tasks again to return updated task list
    tasks = get_todos()
    task_list = [{'id': task[0], 'name': task[1], 'checked': task[2]} for task in tasks]
    
    return jsonify({"tasks": task_list})  # Return updated tasks in JSON format

# Route to Mark a Task as Checked (Completed)
@todo_bp.route('/checked/<int:task_id>', methods=['POST'])
def check_task(task_id):
    # Update the task completion status in your database
    task = get_todos()  # Assuming this function gets all tasks, you need to implement the logic for updating completion status.
    update_task(task_id, task[0][1])  # Example: This might require changing logic
    return redirect(url_for('todo_bp.home'))

# Route to Edit a Task (Show Edit Page)
@todo_bp.route('/edit/<int:task_id>', methods=['GET'])
def edit_task(task_id):
    task = get_todos()  # Fetch the task by task_id
    task_to_edit = next((t for t in task if t[0] == task_id), None)
    return render_template('edit.html', task=task_to_edit)

# Route to Update the Task
@todo_bp.route('/edit/<int:task_id>', methods=['POST'])
def update_task_route(task_id):
    task_name = request.form.get('todo_name')
    if not task_name:
        return redirect(url_for('todo_bp.home'))  # Redirect if no task name
    
    update_task(task_id, task_name)
    return redirect(url_for('todo_bp.home'))  # Redirect back to home page

# Route to Delete a Task
@todo_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    # Delete the task from PostgreSQL
    delete_task(task_id)
    return redirect(url_for('todo_bp.home'))  # Redirect back to home page

# Route to Delete All Tasks (optional)
@todo_bp.route('/todos', methods=['DELETE'])
def delete_all_tasks_route():
    # Delete all tasks from PostgreSQL
    delete_all_tasks()
    return redirect(url_for('todo_bp.home'))  # Redirect to home after deleting all tasks
