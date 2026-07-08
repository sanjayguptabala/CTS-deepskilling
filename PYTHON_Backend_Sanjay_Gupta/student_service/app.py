import os
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), "student_service.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='unique_student_course_enrollment'),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id
        }

# Initialise tables
with app.app_context():
    db.create_all()

# Helper Response
def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code

@app.route('/api/students/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return make_response_json([s.to_dict() for s in students], 200)

@app.route('/api/students/', methods=['POST'])
def create_student():
    data = request.get_json() or {}
    for f in ['first_name', 'last_name', 'email']:
        if f not in data:
            return jsonify({'status': 'error', 'message': f'Missing field: {f}'}), 400
            
    if Student.query.filter_by(email=data['email']).first():
        return jsonify({'status': 'error', 'message': 'Student with email already exists'}), 400
        
    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    db.session.add(new_student)
    db.session.commit()
    return make_response_json(new_student.to_dict(), 201)

@app.route('/api/students/<int:student_id>/', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404
    return make_response_json(student.to_dict(), 200)

@app.route('/api/students/<int:student_id>/', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404
    data = request.get_json() or {}
    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.email = data.get('email', student.email)
    db.session.commit()
    return make_response_json(student.to_dict(), 200)

@app.route('/api/students/<int:student_id>/', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404
    db.session.delete(student)
    db.session.commit()
    return make_response_json({'message': 'Student deleted'}, 200)

@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404
        
    data = request.get_json() or {}
    course_id = data.get('course_id')
    if not course_id:
        return jsonify({'status': 'error', 'message': 'Missing field: course_id'}), 400
        
    # Synchronous Inter-Service Communication to verify course exists
    course_service_url = f"http://127.0.0.1:5001/api/courses/{course_id}/"
    try:
        response = requests.get(course_service_url, timeout=5)
    except requests.exceptions.ConnectionError:
        return jsonify({
            'status': 'error',
            'message': 'Course Service is currently unavailable. Please try again later.'
        }), 503
        
    if response.status_code == 404:
        return jsonify({
            'status': 'error',
            'message': f'Course with id {course_id} does not exist.'
        }), 400
    elif response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while validating the course with Course Service.'
        }), 500
        
    # Check if student is already enrolled
    existing = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if existing:
        return jsonify({
            'status': 'error',
            'message': 'Student is already enrolled in this course.'
        }), 400
        
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return make_response_json(enrollment.to_dict(), 201)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002)
