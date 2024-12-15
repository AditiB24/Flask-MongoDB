from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import random

app = Flask(__name__)

# # MongoDB setup
# client = MongoClient('mongodb+srv://bhilareaditi24:bhilareaditi24@aditib.qs572.mongodb.net/?retryWrites=true&w=majority&appName=AditiB')
# db = client.AditiB
# todos_collection = db.todos

import psycopg2
import os

# Get PostgreSQL URI from environment variables (as a security best practice)
DATABASE_URL = os.getenv('postgresql://dim_v4xu_user:27vlIxoz9ed6C7JPeS5IXE5E47tvV78t@dpg-ctfgso56l47c73b8lm80-a.oregon-postgres.render.com/dim_v4xu')

# Connect to your PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Example: Creating a table (if needed)
cursor.execute('''CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100),
                    completed BOOLEAN
                  );''')

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        todo_name = request.form["todo_name"]
        cur_id = random.randint(1, 1000)
        # Insert new task into MongoDB
        todos_collection.insert_one(
            {
                'id': cur_id,
                'name': todo_name,
                'checked': False
            }
        )
        return redirect(url_for("home"))
    
    # Fetch all tasks from MongoDB
    todos = list(todos_collection.find())
    return render_template("index.html", items=todos)

@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    # Toggle the 'checked' status of a task
    todos_collection.update_one(
        {'id': todo_id},
        {'$set': {'checked': {'$not': '$checked'}}}
    )
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    # Delete a task from MongoDB
    todos_collection.delete_one({'id': todo_id})
    return redirect(url_for("home"))

@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit_todo(todo_id):
    if request.method == "POST":
        new_name = request.form["todo_name"]
        # Update task in MongoDB
        todos_collection.update_one(
            {'id': todo_id},
            {'$set': {'name': new_name}}
        )
        return redirect(url_for("home"))

    # Fetch the task to edit from MongoDB
    task = todos_collection.find_one({'id': todo_id})
    return render_template("edit.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)
