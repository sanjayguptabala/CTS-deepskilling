class Config:
    SECRET_KEY = 'dev-secret-key'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_coursemanager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
