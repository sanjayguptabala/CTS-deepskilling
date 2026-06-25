# Request Lifecycle

# Browser sends GET /api/courses/

# Request -> Middleware -> URL Router
# URL Router -> View
# View -> Model
# Model -> Database
# Database -> View
# View -> Response
# Response -> Browser


# Middleware

# AuthenticationMiddleware:
# Identifies logged in users

# SecurityMiddleware:
# Adds security headers and HTTPS


# WSGI

# Synchronous request handling


# ASGI

# Asynchronous request handling
# Supports WebSockets and realtime applications


# MVC

# Model -> Model
# View -> Template
# Controller -> Django View


# MVT

# Model -> Database

# View -> Business logic

# Template -> UI