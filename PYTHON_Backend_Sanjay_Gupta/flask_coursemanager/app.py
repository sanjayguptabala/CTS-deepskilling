from flask import Flask, jsonify
from config import Config
from extensions import db, migrate
from courses.routes import courses_bp

# Import models so Flask-Migrate registers them for migrations detection
from courses.models import Department, Course, Student, Enrollment

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprint
    app.register_blueprint(courses_bp)
    
    # Global JSON error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'message': 'An internal server error occurred'
        }), 500
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000)
