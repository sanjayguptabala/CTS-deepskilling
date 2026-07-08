import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), "course_service.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {"id": self.id, "name": self.name}

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits,
            "department_id": self.department_id
        }

# Initialise tables and seed default departments
with app.app_context():
    db.create_all()
    if not Department.query.filter_by(id=1).first():
        db.session.add(Department(id=1, name="Computer Science"))
    if not Department.query.filter_by(id=2).first():
        db.session.add(Department(id=2, name="Mathematics"))
    db.session.commit()

# Helper Response
def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code

@app.route('/api/courses/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return make_response_json([c.to_dict() for c in courses], 200)

@app.route('/api/courses/', methods=['POST'])
def create_course():
    data = request.get_json() or {}
    for f in ['name', 'code', 'credits', 'department_id']:
        if f not in data:
            return jsonify({'status': 'error', 'message': f'Missing field: {f}'}), 400
            
    if Course.query.filter_by(code=data['code']).first():
        return jsonify({'status': 'error', 'message': 'Course code already exists'}), 400
        
    new_course = Course(
        name=data['name'],
        code=data['code'],
        credits=data['credits'],
        department_id=data['department_id']
    )
    db.session.add(new_course)
    db.session.commit()
    return make_response_json(new_course.to_dict(), 201)

@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    return make_response_json(course.to_dict(), 200)

@app.route('/api/courses/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    data = request.get_json() or {}
    course.name = data.get('name', course.name)
    course.code = data.get('code', course.code)
    course.credits = data.get('credits', course.credits)
    course.department_id = data.get('department_id', course.department_id)
    db.session.commit()
    return make_response_json(course.to_dict(), 200)

@app.route('/api/courses/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    db.session.delete(course)
    db.session.commit()
    return make_response_json({'message': 'Course deleted'}, 200)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
