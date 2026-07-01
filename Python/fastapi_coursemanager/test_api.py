import urllib.request
import urllib.error
import json

def make_request(url, method='GET', data=None, headers=None):
    if headers is None:
        headers = {}
    if data is not None:
        data_bytes = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    else:
        data_bytes = None
        
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers=headers,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            resp_headers = response.info()
            body = response.read().decode('utf-8')
            return status, json.loads(body) if body else None, resp_headers
    except urllib.error.HTTPError as e:
        status = e.code
        resp_headers = e.info()
        body = e.read().decode('utf-8')
        return status, json.loads(body) if body else None, resp_headers
    except Exception as e:
        print(f"Connection/Unexpected error: {e}")
        return None, None, None

def run_tests():
    base_url = "http://127.0.0.1:8000"

    print("--- Test 1: Root Route ---")
    status, body, headers = make_request(f"{base_url}/")
    print(f"Status: {status}, Body: {body}")
    assert status == 200
    assert body == {"message": "API running"}
    print("Test 1 Passed!\n")

    print("--- Test 2a: Register User ---")
    user_credentials = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    status, body, headers = make_request(f"{base_url}/api/v1/auth/register/", method='POST', data=user_credentials)
    print(f"Status: {status}, Body: {body}, Headers: {headers.get('Location')}")
    assert status == 201
    assert body["email"] == "testuser@example.com"
    assert "hashed_password" not in body
    assert headers.get('Location') == '/api/v1/auth/register/'
    print("Test 2a Passed!\n")

    print("--- Test 2b: Register Duplicate User (409 Conflict) ---")
    status, body, headers = make_request(f"{base_url}/api/v1/auth/register/", method='POST', data=user_credentials)
    print(f"Status: {status}, Body: {body}")
    assert status == 409
    assert body["error"]["code"] == "CONFLICT"
    assert "already registered" in body["error"]["message"]
    print("Test 2b Passed!\n")

    print("--- Test 2c: Login to get Access Token ---")
    status, body, headers = make_request(f"{base_url}/api/v1/auth/login/", method='POST', data=user_credentials)
    print(f"Status: {status}, Body: {body}")
    assert status == 200
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    auth_token = body["access_token"]
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
    print("Test 2c Passed!\n")

    print("--- Test 2d: POST Course without Token (401 Unauthorized) ---")
    valid_course = {
        "name": "Python Backend Development",
        "code": "PY-101",
        "credits": 4,
        "department_id": 1
    }
    status, body, headers = make_request(f"{base_url}/api/v1/courses/", method='POST', data=valid_course)
    print(f"Status: {status}, Body: {body}")
    assert status == 401
    assert body["error"]["code"] == "UNAUTHORIZED"
    print("Test 2d Passed!\n")

    print("--- Test 2: POST /api/v1/courses/ (Valid Data with Token) ---")
    status, body, headers = make_request(f"{base_url}/api/v1/courses/", method='POST', data=valid_course, headers=auth_headers)
    print(f"Status: {status}, Body: {body}, Location Header: {headers.get('Location')}")
    assert status == 201
    assert body["name"] == "Python Backend Development"
    assert body["code"] == "PY-101"
    course_id = body["id"]
    assert headers.get('Location') == f'/api/v1/courses/{course_id}/'
    print("Test 2 Passed!\n")

    print("--- Test 3: POST /api/v1/courses/ (Missing Fields) ---")
    invalid_course = {
        "name": "Python Backend Development",
        "code": "PY-101"
    }
    status, body, headers = make_request(f"{base_url}/api/v1/courses/", method='POST', data=invalid_course, headers=auth_headers)
    print(f"Status: {status}, Body: {body}")
    assert status == 422
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert "credits" in body["error"]["message"]
    print("Test 3 Passed!\n")

    print("--- Test 4: GET /api/v1/courses/{id} (Valid ID) ---")
    status, body, headers = make_request(f"{base_url}/api/v1/courses/{course_id}")
    print(f"Status: {status}, Body: {body}")
    assert status == 200
    assert body["id"] == course_id
    print("Test 4 Passed!\n")

    print("--- Test 5: GET /api/v1/courses/{id} (Invalid ID 404 Check) ---")
    status, body, headers = make_request(f"{base_url}/api/v1/courses/99999")
    print(f"Status: {status}, Body: {body}")
    assert status == 404
    assert body["error"]["code"] == "NOT_FOUND"
    assert "Course not found" in body["error"]["message"]
    print("Test 5 Passed!\n")

    print("--- Test 6a: PATCH /api/v1/courses/{id} (Valid Partial Update) ---")
    patch_data = {
        "name": "Advanced Python Backend"
    }
    status, body, headers = make_request(f"{base_url}/api/v1/courses/{course_id}", method='PATCH', data=patch_data)
    print(f"Status: {status}, Body: {body}")
    assert status == 200
    assert body["name"] == "Advanced Python Backend"
    assert body["code"] == "PY-101"
    print("Test 6a Passed!\n")

    print("--- Test 6b: PUT /api/v1/courses/{id} (Invalid Partial Update -> 422 Check) ---")
    status, body, headers = make_request(f"{base_url}/api/v1/courses/{course_id}", method='PUT', data=patch_data)
    print(f"Status: {status}, Body: {body}")
    assert status == 422
    assert body["error"]["code"] == "VALIDATION_ERROR"
    print("Test 6b Passed!\n")

    print("--- Test 6c: PUT /api/v1/courses/{id} (Valid Full Replace) ---")
    full_replace_data = {
        "name": "Fully Replaced Python Backend",
        "code": "PY-101-NEW",
        "credits": 5,
        "department_id": 1
    }
    status, body, headers = make_request(f"{base_url}/api/v1/courses/{course_id}", method='PUT', data=full_replace_data)
    print(f"Status: {status}, Body: {body}")
    assert status == 200
    assert body["name"] == "Fully Replaced Python Backend"
    assert body["code"] == "PY-101-NEW"
    assert body["credits"] == 5
    print("Test 6c Passed!\n")

    print("--- Test 6d: GET Pagination and Search ---")
    status, body, headers = make_request(f"{base_url}/api/v1/courses/?page=1&page_size=1&search=Replace")
    print(f"Status: {status}, Body: {body}")
    assert status == 200
    assert "count" in body
    assert "results" in body
    assert len(body["results"]) == 1
    assert "Replaced" in body["results"][0]["name"]
    print("Test 6d Passed!\n")

    print("--- Test 7: Student CRUD: Create Student ---")
    student_data = {
        "first_name": "Shiva",
        "last_name": "Kumar",
        "email": "shiva@gmail.com"
    }
    status, body, headers = make_request(f"{base_url}/api/v1/students/", method='POST', data=student_data)
    print(f"Status: {status}, Body: {body}, Location Header: {headers.get('Location')}")
    assert status == 201
    assert body["first_name"] == "Shiva"
    assert body["email"] == "shiva@gmail.com"
    student_id = body["id"]
    assert headers.get('Location') == f'/api/v1/students/{student_id}/'
    print("Test 7 Passed!\n")

    print("--- Test 8: Student CRUD: Create Duplicate Email ---")
    status, body, headers = make_request(f"{base_url}/api/v1/students/", method='POST', data=student_data)
    print(f"Status: {status}, Body: {body}")
    assert status == 400
    assert body["error"]["code"] == "BAD_REQUEST"
    assert "already exists" in body["error"]["message"]
    print("Test 8 Passed!\n")

    print("--- Test 9: Student CRUD: Get Student ---")
    status, body, headers = make_request(f"{base_url}/api/v1/students/{student_id}")
    print(f"Status: {status}, Body: {body}")
    assert status == 200
    assert body["id"] == student_id
    print("Test 9 Passed!\n")

    print("--- Test 10: Student CRUD: Get Invalid Student ---")
    status, body, headers = make_request(f"{base_url}/api/v1/students/99999")
    print(f"Status: {status}, Body: {body}")
    assert status == 404
    assert body["error"]["code"] == "NOT_FOUND"
    assert "Student not found" in body["error"]["message"]
    print("Test 10 Passed!\n")

    print("--- Test 11: Student CRUD: Update Student ---")
    student_update = {
        "last_name": "Reddy"
    }
    status, body, headers = make_request(f"{base_url}/api/v1/students/{student_id}", method='PUT', data=student_update)
    print(f"Status: {status}, Body: {body}")
    assert status == 200
    assert body["last_name"] == "Reddy"
    print("Test 11 Passed!\n")

    print("--- Test 12: Enrollment CRUD: Create Enrollment (Valid) ---")
    enrollment_data = {
        "student_id": student_id,
        "course_id": course_id
    }
    status, body, headers = make_request(f"{base_url}/api/v1/enrollments/", method='POST', data=enrollment_data)
    print(f"Status: {status}, Body: {body}, Location Header: {headers.get('Location')}")
    assert status == 201
    assert body["student_id"] == student_id
    assert body["course_id"] == course_id
    enrollment_id = body["id"]
    assert headers.get('Location') == f'/api/v1/enrollments/{enrollment_id}/'
    print("Test 12 Passed!\n")

    print("--- Test 13: Enrollment CRUD: Duplicate Enrollment ---")
    status, body, headers = make_request(f"{base_url}/api/v1/enrollments/", method='POST', data=enrollment_data)
    print(f"Status: {status}, Body: {body}")
    assert status == 400
    assert body["error"]["code"] == "BAD_REQUEST"
    assert "already enrolled" in body["error"]["message"]
    print("Test 13 Passed!\n")

    print("--- Test 14: Enrollment CRUD: Create Enrollment (Invalid Student) ---")
    invalid_enrollment = {
        "student_id": 99999,
        "course_id": course_id
    }
    status, body, headers = make_request(f"{base_url}/api/v1/enrollments/", method='POST', data=invalid_enrollment)
    print(f"Status: {status}, Body: {body}")
    assert status == 400
    assert body["error"]["code"] == "BAD_REQUEST"
    assert "Student with id 99999 does not exist." in body["error"]["message"]
    print("Test 14 Passed!\n")

    print("--- Test 15: Course Enrollments (Join Query) ---")
    status, body, headers = make_request(f"{base_url}/api/v1/courses/{course_id}/students/")
    print(f"Status: {status}, Body: {body}")
    assert status == 200
    assert isinstance(body, list)
    assert len(body) >= 1
    assert body[0]["id"] == student_id
    assert body[0]["first_name"] == "Shiva"
    print("Test 15 Passed!\n")

    print("--- Test 16: Delete Enrollment ---")
    status, body, headers = make_request(f"{base_url}/api/v1/enrollments/{enrollment_id}", method='DELETE')
    print(f"Status: {status}, Body: {body}")
    assert status == 204
    assert body is None
    print("Test 16 Passed!\n")

    print("--- Test 17: Delete Course (Verify 204 No Content with Token) ---")
    status, body, headers = make_request(f"{base_url}/api/v1/courses/{course_id}", method='DELETE', headers=auth_headers)
    print(f"Status: {status}, Body: {body}")
    assert status == 204
    assert body is None
    print("Test 17 Passed!\n")

    print("--- Test 18: Delete Course (Already Deleted -> 404 Check) ---")
    status, body, headers = make_request(f"{base_url}/api/v1/courses/{course_id}", method='DELETE', headers=auth_headers)
    print(f"Status: {status}, Body: {body}")
    assert status == 404
    assert body["error"]["code"] == "NOT_FOUND"
    assert "Course not found" in body["error"]["message"]
    print("Test 18 Passed!\n")

    print("--- Test 19: Delete Student (Verify 204) ---")
    status, body, headers = make_request(f"{base_url}/api/v1/students/{student_id}", method='DELETE')
    print(f"Status: {status}, Body: {body}")
    assert status == 204
    assert body is None
    print("Test 19 Passed!\n")

    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
