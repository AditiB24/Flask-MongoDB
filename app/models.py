import os
from pymongo import MongoClient

# Fetch MongoDB URI from environment variables or use localhost as fallback
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://bhilareaditi24:<db_password>@aditib.qs572.mongodb.net/?retryWrites=true&w=majority&appName=AditiB")
client = MongoClient(mongo_uri)

# Connect to your database
db = client["todo_app"]
todos_collection = db["todos"]
