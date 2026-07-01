import requests
from flask import Flask, request, Response

app = Flask(__name__)

COURSE_SERVICE_URL = "http://127.0.0.1:5001"
STUDENT_SERVICE_URL = "http://127.0.0.1:5002"

@app.route('/api/courses/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/api/courses/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def courses_proxy(path):
    url = f"{COURSE_SERVICE_URL}/api/courses/{path}"
    if request.query_string:
        url += f"?{request.query_string.decode('utf-8')}"
    return proxy_request(url)

@app.route('/api/students/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/api/students/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def students_proxy(path):
    url = f"{STUDENT_SERVICE_URL}/api/students/{path}"
    if request.query_string:
        url += f"?{request.query_string.decode('utf-8')}"
    return proxy_request(url)

def proxy_request(url):
    # Forward the headers, skipping the host header to ensure correct routing
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10
        )
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": "Backend service is unreachable"}, 503

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers]
    
    return Response(resp.content, resp.status_code, headers)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
