from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import random

app = Flask(__name__)

# Get PostgreSQL URI from environment variables (as a security best practice)
DATABASE_URL = os.getenv('postgresql://dim_v4xu_user:27vlIxoz9ed6C7JPeS5IXE5E47tvV78t@dpg-ctfgso56l47c73b8lm80-a.oregon-postgres.render.com/dim_v4xu')

# Connect to your PostgreSQL database
def create_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        todo_name = request.form["todo_name"]
        cur_id = random.randint(1, 1000)
        
        # Insert new task into PostgreSQL
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO todos (title, completed) VALUES (%s, %s);''', (todo_name, False))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for("home"))
    
    # Fetch all tasks from PostgreSQL
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM todos;''')
    todos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("index.html", items=todos)

@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    # Toggle the 'checked' status of a task in PostgreSQL
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE todos SET completed = NOT completed WHERE id = %s;''', (todo_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    # Delete a task from PostgreSQL
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM todos WHERE id = %s;''', (todo_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("home"))

@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit_todo(todo_id):
    if request.method == "POST":
        new_name = request.form["todo_name"]
        
        # Update task in PostgreSQL
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''UPDATE todos SET title = %s WHERE id = %s;''', (new_name, todo_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for("home"))

    # Fetch the task to edit from PostgreSQL
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM todos WHERE id = %s;''', (todo_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("edit.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
