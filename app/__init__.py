from flask import Flask
from app.routes import todo_bp
import psycopg2
import os

def create_app():
    app = Flask(__name__)

    # Configure PostgreSQL URI
    # app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://new_project_8fzg_user:LJke8zkvYQYdLnkVuhoBEfxMDQ8dNshG@dpg-ctfrlvt2ng1s738mfcag-a.singapore-postgres.render.com/new_project_8fzg')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
    # Register Blueprints (routes)
    app.register_blueprint(todo_bp)

    return app

