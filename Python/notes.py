"""
HANDS-ON 1: Web Framework Foundations & Django Project Setup

1) Request-Response Cycle for GET /api/courses/

Browser
  -> sends GET /api/courses/
  -> Django URL router matches the path in urls.py
  -> mapped View function/class is called
  -> View may ask the Model for data
  -> Model runs a database query and returns results
  -> View formats the data into an HTTP response
  -> Django sends the response back to the browser

2) Middleware in the cycle

Middleware sits between the request and the view, and again between the view and the response.
It can inspect, modify, or reject a request before it reaches the view, and it can also change the
response before it is sent back to the client.

Two built-in Django middleware classes:
- django.middleware.security.SecurityMiddleware: adds security-related headers and helps enforce
  security settings such as HTTPS behavior.
- django.contrib.sessions.middleware.SessionMiddleware: enables session support so Django can store
  and read session data per user.

3) WSGI vs ASGI

WSGI = Web Server Gateway Interface.
It is the traditional Python web server interface for synchronous request handling.
Django uses WSGI by default for classic sync deployments.

ASGI = Asynchronous Server Gateway Interface.
It supports async request handling, long-lived connections, websockets, and other concurrent I/O use
cases.
Switch to ASGI when you need async views, websockets, background streaming, or other concurrent
communication patterns.

4) MVC and Django's MVT mapping

MVC = Model-View-Controller
- Model: data and business rules
- View: the UI layer that presents data
- Controller: handles input, updates models, and chooses the response

Django uses MVT = Model-View-Template
- Model: same as MVC Model
- View: acts like the MVC Controller because it handles requests, applies logic, and selects data
- Template: acts like the MVC View because it renders the final presentation

So the main mapping is:
- MVC Model -> Django Model
- MVC View -> Django Template
- MVC Controller -> Django View

For the request flow above, Django's View is the control layer that sits between routing and rendering,
while the Template is responsible for presentation.
"""