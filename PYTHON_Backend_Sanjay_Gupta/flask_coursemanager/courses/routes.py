from flask import Blueprint, jsonify, request
from extensions import db
from courses.models import Course, Student, Enrollment

# Define the blueprint with prefix /api/courses
courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

def make_response_json(data, status_code=200):
    """
    Helper function that returns a consistent JSON envelope.
    """
    return jsonify({
        'status': 'success',
        'data': data
    }), status_code

@courses_bp.route('/', methods=['GET'], strict_slashes=False)
def get_courses():
    courses = Course.query.all()
    serialized = [c.to_dict() for c in courses]
    return make_response_json(serialized, 200)

@courses_bp.route('/', methods=['POST'], strict_slashes=False)
def create_course():
    data = request.get_json()
    if data is None:
        return jsonify({
            'status': 'error',
            'message': 'Request body must be JSON'
        }), 400
    
    # Validate required fields
    required_fields = ['name', 'code', 'credits', 'department_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({
            'status': 'error',
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400
        
    # Check duplicate code
    if Course.query.filter_by(code=data['code']).first():
        return jsonify({
            'status': 'error',
            'message': f"Course with code {data['code']} already exists"
        }), 400
    
    new_course = Course(
        name=data.get("name"),
        code=data.get("code"),
        credits=data.get("credits"),
        department_id=data.get("department_id")
    )
    db.session.add(new_course)
    db.session.commit()
    return make_response_json(new_course.to_dict(), 201)

@courses_bp.route('/<int:course_id>/', methods=['GET'], strict_slashes=False)
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return make_response_json(course.to_dict(), 200)

@courses_bp.route('/<int:course_id>/', methods=['PUT'], strict_slashes=False)
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    data = request.get_json()
    if data is None:
        return jsonify({
            'status': 'error',
            'message': 'Request body must be JSON'
        }), 400
    
    # Update fields if present in input
    course.name = data.get('name', course.name)
    course.code = data.get('code', course.code)
    course.credits = data.get('credits', course.credits)
    if 'department_id' in data:
        course.department_id = data['department_id']
        
    db.session.commit()
    return make_response_json(course.to_dict(), 200)

@courses_bp.route('/<int:course_id>/', methods=['DELETE'], strict_slashes=False)
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return make_response_json({'message': f'Course {course_id} has been deleted successfully'}, 200)

@courses_bp.route('/<int:course_id>/students/', methods=['GET'], strict_slashes=False)
def get_course_students(course_id):
    # Verify course exists
    course = Course.query.get_or_404(course_id)
    
    # Perform JOIN query to fetch students enrolled in the specified course
    students = db.session.query(Student).join(Enrollment).filter(Enrollment.course_id == course_id).all()
    
    serialized_students = [s.to_dict() for s in students]
    return make_response_json(serialized_students, 200)
