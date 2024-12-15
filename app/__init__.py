# app/__init__.py
from flask import Flask
from app.models import mongo
from app.routes import todo_bp

def create_app():
    app = Flask(__name__)

    # Configure MongoDB URI (Adjust this if you have a different database setup)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/todo_db'  # Use your own MongoDB URI

    mongo.init_app(app)

    # Register Blueprints (routes)
    app.register_blueprint(todo_bp)

    return app
