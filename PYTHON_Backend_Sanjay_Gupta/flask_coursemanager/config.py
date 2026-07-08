import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'flask-insecure-secret-key-1234')
    # Use SQLite database file inside the project directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///flask_db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
