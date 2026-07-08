# notes.py
# ==============================================================================
# Django Web Framework Foundations - Conceptual Notes
# ==============================================================================

"""
TASK 1: UNDERSTAND THE REQUEST-RESPONSE CYCLE

--------------------------------------------------------------------------------
1. Journey of a GET /api/courses/ Request through a Django Application
--------------------------------------------------------------------------------

[ Browser / Client ] 
        │  (Sends HTTP GET /api/courses/ request)
        ▼
[ Web Server (e.g., Nginx / Gunicorn / Daphne) ]
        │  (Receives request, translates to WSGI/ASGI environ dictionary)
        ▼
[ wsgi.py / asgi.py (Django Entry Point) ]
        │  (Invokes Django handler)
        ▼
┌────────────────────────────────────────────────────────┐
│ MIDDLEWARE STACK (Request Phase - Top to Bottom)       │
│ - SecurityMiddleware                                   │
│ - SessionMiddleware                                    │
│ - CommonMiddleware                                     │
│ - CsrfViewMiddleware                                   │
│ - AuthenticationMiddleware                             │
│ - MessageMiddleware                                    │
└──────────────────────────┬─────────────────────────────┘
                           │  (Processes/Enriches Request)
                           ▼
[ URL Router / URLconf (urls.py) ]
  - Compares the path `/api/courses/` against patterns.
  - Matches the URL to a specific view function or class-based view.
        │  (Resolves view and arguments)
        ▼
┌────────────────────────────────────────────────────────┐
│ MIDDLEWARE STACK (View Middleware Hook - Optional)     │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
[ View (Controller logic) ]
  - Takes the HttpRequest object.
  - Formulates query logic to retrieve list of courses.
        │  (Calls Model ORM methods, e.g., Course.objects.all())
        ▼
[ Model (Database Layer & ORM) ]
  - Translates the ORM call to SQL: `SELECT * FROM course_table;`.
  - Queries the Database.
        │  (Returns DB results)
        ▼
[ View (Processes Database Results) ]
  - Receives Python objects from Model.
  - Serializes to JSON/XML (e.g., for API) OR renders an HTML template.
  - Constructs and returns an HttpResponse (or JsonResponse) object.
        │  (Returns Response)
        ▼
┌────────────────────────────────────────────────────────┐
│ MIDDLEWARE STACK (Response Phase - Bottom to Top)      │
│ - MessageMiddleware                                    │
│ - AuthenticationMiddleware                             │
│ - CsrfViewMiddleware                                   │
│ - CommonMiddleware                                     │
│ - SessionMiddleware                                    │
│ - SecurityMiddleware                                    │
└──────────────────────────┬─────────────────────────────┘
                           │  (Modifies response headers/cookies/etc.)
                           ▼
[ wsgi.py / asgi.py ]
        │  (Returns response back to Web Server)
        ▼
[ Web Server ]
        │  (Sends HTTP 200 OK Response with JSON/HTML payload)
        ▼
[ Browser / Client ] (Renders courses interface to user)


--------------------------------------------------------------------------------
2. Where Middleware Sits & Two Built-in Middleware Classes
--------------------------------------------------------------------------------

Where it sits:
- Middleware sits between Django's entry handler (WSGI/ASGI handler) and the 
  URL Router/View.
- It functions as a bi-directional chain of hooks. It runs sequentially from 
  top-to-bottom on incoming requests (before reaching the view), and from 
  bottom-to-top on outgoing responses (after leaving the view).

Two Built-in Django Middleware Classes:
1. `django.middleware.security.SecurityMiddleware`:
   - What it does: Provides several security enhancements for the request/response 
     cycle. It sets headers such as `X-Frame-Options` (to prevent clickjacking), 
     `X-Content-Type-Options` (to prevent MIME type sniffing), and handles SSL 
     redirects (forcing HTTP requests to redirect to HTTPS).
     
2. `django.contrib.sessions.middleware.SessionMiddleware`:
   - What it does: Enables session support across requests. For an incoming 
     request, it reads the session cookie (usually `sessionid`), fetches the 
     corresponding session data from the configured storage (DB, cache, or files), 
     and attaches it as `request.session`. For an outgoing response, it updates 
     the storage and sets the session cookie back to the client if needed.


--------------------------------------------------------------------------------
3. WSGI vs ASGI
--------------------------------------------------------------------------------

WSGI (Web Server Gateway Interface):
- Nature: Synchronous.
- Design: Designed to handle one request per thread/process at a time. It blocks 
  while waiting for database queries or network requests to complete.
- Default: Django uses WSGI by default (`wsgi.py` handles requests, and the default 
  development server `runserver` runs in a synchronous WSGI context).

ASGI (Asynchronous Server Gateway Interface):
- Nature: Asynchronous.
- Design: Built on top of Python's `asyncio`. It handles concurrent connections 
  without blocking threads, making it highly efficient for persistent, 
  long-lived connections.
- When to switch to ASGI:
  1. Real-time features: When you need WebSockets (e.g., chat systems, real-time dashboards).
  2. Server-Sent Events (SSE): When pushing continuous updates to the browser.
  3. High-concurrency tasks: When you have many long-polling requests, long-running 
     file uploads, or concurrent API requests where async database adapters or 
     network requests are used to prevent thread starvation.
  - To use ASGI in production, you would run your Django project using an ASGI 
    server like Daphne or Uvicorn rather than Gunicorn/uWSGI.


--------------------------------------------------------------------------------
4. MVC (Model-View-Controller) vs MVT (Model-View-Template) Mapping
--------------------------------------------------------------------------------

In traditional MVC software design:
- Model (M): Manages data structure, schema validation, and database operations.
- View (V): The presentation layer shown to the user (HTML/CSS/UI).
- Controller (C): Receives user inputs (clicks/requests), processes business logic, 
  queries the Model, and determines which View should render.

In Django's MVT implementation:
- Model (M) ──► Maps directly to Django's **Model**
  - Defines the database schema, validations, and ORM query structures.
  
- View (V)  ──► Maps to Django's **Template (T)**
  - Composed of HTML, CSS, JavaScript, and Django Template Language (DTL) tags. 
    It defines exactly how data is structured and presented to the end user.
    
- Controller (C) ──► Maps to Django's **View (V)**
  - Contains the Python logic. It receives HTTP requests, calls models or 
    external APIs, computes context dictionary parameters, and returns 
    the rendered Template or raw responses (like JsonResponse/HttpResponse).
    
*Note: The Routing engine (URLconf / `urls.py`) works closely with Django's View 
to act as the front controller dispatcher.*

--------------------------------------------------------------------------------
5. Django Project vs. Django App
--------------------------------------------------------------------------------

- Django Project:
  - Definition: The overall project/website configuration.
  - Role: Acts as the top-level orchestrator. It manages the global settings.py, 
    main urls.py routes, database connections, and WSGI/ASGI entry configurations.
  - Scope: A project defines the execution environment and specifies which modular 
    components (apps) are activated together.

- Django App:
  - Definition: A self-contained, reusable module or Python package created to 
    handle a single feature set or business domain (e.g., courses, authentication, blog).
  - Role: Contains its own logic, defining its own models, views, templates, tests, 
    and sub-routing.
  - Scope: An app is designed to be decoupled so that it can be reused in other 
    Django projects.

- Relationship:
  - One-to-Many: A single Django project can host/register many Django apps 
    (e.g., a school project could contain a 'courses' app, a 'billing' app, and a 
    'forum' app).


--------------------------------------------------------------------------------
6. Django ORM Key Concepts & Query Optimization
--------------------------------------------------------------------------------

- ForeignKey Span Lookups (Double Underscore `__`):
  - Purpose: Performs a SQL JOIN across a foreign key relationship to filter or access 
    fields on related models.
  - Example: `Course.objects.filter(department__name='Computer Science')` translates 
    to a SQL `INNER JOIN` between the `courses_course` and `courses_department` tables 
    to filter courses based on the department's name field.

- Annotation and Aggregation:
  - Purpose: Computes summary metrics (such as sums, counts, averages) on related tables 
    in the database.
  - Example: `Department.objects.annotate(course_count=Count('course'))` dynamically 
    attaches a `course_count` attribute to each Department object by executing a SQL 
    `LEFT OUTER JOIN` and `GROUP BY` clause. This allows fetching the number of courses 
    per department efficiently in a single query.

- Preventing the N+1 Query Problem with `select_related`:
  - Problem: If you fetch N objects (e.g., Students) and loop through them to access a 
    ForeignKey field (e.g., their Department), Django will run 1 query to fetch the students 
    and then N individual queries to fetch the department details for each student. This is 
    extremely inefficient (N+1 queries).
  - Solution: Use `select_related('department')`. This tells Django to run a single 
    query with an `INNER JOIN` or `LEFT OUTER JOIN` to fetch the related model fields upfront.
  - SQL verification:
    `SELECT ... FROM "courses_student" INNER JOIN "courses_department" ON ...`
    This retrieves all data in exactly 1 database hit, confirmed via `connection.queries`.

- Database-Level Operations with `F()` Objects:
  - Purpose: Allows referencing a model field directly in the database without 
    pulling the values into Python memory.
  - Benefit 1: Avoids race conditions (concurrency issues) since the database itself handles 
    the current value computation.
  - Benefit 2: Improves performance by avoiding the overhead of fetching, instantiating 
    python objects, modifying, and saving each row individually.
  - Example: `Department.objects.update(budget=F('budget') * 1.1)` generates:
    `UPDATE "courses_department" SET "budget" = ("courses_department"."budget" * 1.1)`
    This execution happens directly at the database engine level.

"""

# Placeholder main check
if __name__ == "__main__":
    print("Django Framework Foundation Notes successfully loaded.")
