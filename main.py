from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)

# PostgreSQL connection setup
DATABASE_URL = os.getenv('postgresql://new_project_8fzg_user:LJke8zkvYQYdLnkVuhoBEfxMDQ8dNshG@dpg-ctfrlvt2ng1s738mfcag-a/new_project_8fzg')

# Ensure the database table exists
def init_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS todos (
                           id SERIAL PRIMARY KEY,
                           title VARCHAR(100),
                           completed BOOLEAN DEFAULT FALSE
                         );''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

init_db()

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        if request.method == "POST":
            todo_name = request.form["todo_name"]
            cursor.execute("INSERT INTO todos (title) VALUES (%s);", (todo_name,))
            conn.commit()
            return redirect(url_for("home"))

        cursor.execute("SELECT * FROM todos;")
        todos = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("index.html", items=todos)

    except Exception as e:
        return f"Error: {e}"

# Route to mark tasks as completed
@app.route("/checked/<int:todo_id>")
def checked(todo_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("UPDATE todos SET completed = NOT completed WHERE id = %s;", (todo_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("home"))

    except Exception as e:
        return f"Error: {e}"

# Route to delete a task
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM todos WHERE id = %s;", (todo_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("home"))

    except Exception as e:
        return f"Error: {e}"

# Flask app runner
if __name__ == "__main__":
    app.run(debug=True)
