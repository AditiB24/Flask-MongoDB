# import os
# from pymongo import MongoClient

# # Fetch MongoDB URI from environment variables or use localhost as fallback
# mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://bhilareaditi24:bhilareaditi24@aditib.qs572.mongodb.net/?retryWrites=true&w=majority&appName=AditiB")
# client = MongoClient(mongo_uri)

# # Connect to your database
# db = client["AditiB"]
# todos_collection = db["todos"]
import psycopg2
import os

DATABASE_URL = os.getenv('postgresql://new_project_8fzg_user:LJke8zkvYQYdLnkVuhoBEfxMDQ8dNshG@dpg-ctfrlvt2ng1s738mfcag-a/new_project_8fzg')

def create_todo(title, completed):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title, completed) VALUES (%s, %s)", (title, completed))
    conn.commit()
    cursor.close()
    conn.close()

def get_todos():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return todos




