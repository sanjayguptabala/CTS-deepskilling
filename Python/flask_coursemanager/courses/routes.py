from flask import Blueprint, jsonify, request, abort

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

COURSES = []


def make_response_json(data, status_code):
    return jsonify({'status': 'success', 'data': data}), status_code


def get_course_or_404(course_id):
    for course in COURSES:
        if course['id'] == course_id:
            return course
    abort(404, description=f'Course with id {course_id} not found')


@courses_bp.get('/')
def list_courses():
    return make_response_json(COURSES, 200)


@courses_bp.post('/')
def create_course():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': 'Request body must be valid JSON'}), 400

    required_fields = ['name', 'code', 'credits']
    missing_fields = [field for field in required_fields if field not in data or data[field] in (None, '')]
    if missing_fields:
        return jsonify({'status': 'error', 'message': f"Missing required fields: {', '.join(missing_fields)}"}), 400

    course = {
        'id': len(COURSES) + 1,
        'name': data.get('name'),
        'code': data.get('code'),
        'credits': data.get('credits'),
    }
    COURSES.append(course)
    return make_response_json(course, 201)


@courses_bp.get('/<int:course_id>/')
def get_course(course_id):
    course = get_course_or_404(course_id)
    return make_response_json(course, 200)


@courses_bp.put('/<int:course_id>/')
def update_course(course_id):
    course = get_course_or_404(course_id)
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': 'Request body must be valid JSON'}), 400

    required_fields = ['name', 'code', 'credits']
    missing_fields = [field for field in required_fields if field not in data or data[field] in (None, '')]
    if missing_fields:
        return jsonify({'status': 'error', 'message': f"Missing required fields: {', '.join(missing_fields)}"}), 400

    course.update(
        {
            'name': data['name'],
            'code': data['code'],
            'credits': data['credits'],
        }
    )
    return make_response_json(course, 200)


@courses_bp.delete('/<int:course_id>/')
def delete_course(course_id):
    course = get_course_or_404(course_id)
    COURSES.remove(course)
    return make_response_json({'message': 'Course deleted successfully'}, 200)
