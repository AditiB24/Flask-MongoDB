import psycopg2
import os

# Fetch the PostgreSQL URL from the environment
# DATABASE_URL = os.getenv('postgresql://new_project_8fzg_user:LJke8zkvYQYdLnkVuhoBEfxMDQ8dNshG@dpg-ctfrlvt2ng1s738mfcag-a.singapore-postgres.render.com/new_project_8fzg')
DATABASE_URL = os.getenv('DATABASE_URL')
# Function to create a new task (insert into the database)
def create_todo(title, completed):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title, completed) VALUES (%s, %s)", (title, completed))
    conn.commit()
    cursor.close()
    conn.close()

# Function to retrieve all tasks
def get_todos():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return todos

# Function to update a task by ID
def update_task(task_id, title):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET title = %s WHERE id = %s", (title, task_id))
    conn.commit()
    cursor.close()
    conn.close()

# Function to delete a task by ID
def delete_task(task_id):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Function to delete all tasks
def delete_all_tasks():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos")
    conn.commit()
    cursor.close()
    conn.close()
