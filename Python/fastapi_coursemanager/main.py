from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Response, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import re
import urllib.parse
from jose import jwt, JWTError

from database import engine, Base, get_db, AsyncSessionLocal
import models
import security
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse, DepartmentResponse,
    StudentCreate, StudentUpdate, StudentResponse,
    EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse,
    CoursePaginationResponse, UserCreate, UserResponse, UserLogin, TokenResponse
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed default departments
    async with AsyncSessionLocal() as session:
        # Check and seed Computer Science (ID = 1)
        result = await session.execute(select(models.Department).filter_by(id=1))
        dept1 = result.scalars().first()
        if not dept1:
            session.add(models.Department(id=1, name="Computer Science"))
            
        # Check and seed Mathematics (ID = 2)
        result = await session.execute(select(models.Department).filter_by(id=2))
        dept2 = result.scalars().first()
        if not dept2:
            session.add(models.Department(id=2, name="Mathematics"))
            
        await session.commit()
    yield

tags_metadata = [
    {
        "name": "Courses",
        "description": "Operations with courses. Can create, retrieve, update, and delete courses.",
    },
    {
        "name": "Students",
        "description": "Operations with students. Manage student profiles.",
    },
    {
        "name": "Enrollments",
        "description": "Enroll students in courses and track registrations.",
    },
    {
        "name": "Departments",
        "description": "Operations with departments.",
    },
    {
        "name": "Auth",
        "description": "User registration and JWT-based login authentication.",
    },
]

app = FastAPI(
    title="Course Management API",
    description="A premium API for managing courses, departments, students, and enrollments.",
    version="1.0",
    contact={
        "name": "Sanjay Gupta",
        "email": "sanjay.gupta@example.com"
    },
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

# Configure CORS to allow requests from http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standardized Error response handlers
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_SERVER_ERROR"
    }
    code = code_map.get(exc.status_code, "ERROR")
    message = exc.detail
    if isinstance(exc.detail, dict) and "message" in exc.detail:
        message = exc.detail["message"]
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "field": getattr(exc, "field", None)
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_messages = []
    first_field = None
    for err in errors:
        loc = " -> ".join(str(x) for x in err.get("loc", []))
        msg = err.get("msg", "invalid value")
        error_messages.append(f"{loc}: {msg}")
        if not first_field and err.get("loc"):
            first_field = str(err["loc"][-1])
            
    message = "Validation failed: " + "; ".join(error_messages)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": message,
                "field": first_field
            }
        }
    )

# OAuth2 Password Bearer Scheme for JWT Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(models.User).filter_by(email=email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

@app.get('/')
def read_root():
    return {'message': 'API running'}

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post('/api/v1/auth/register/', response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(user: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    # Validate email format
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if not email_regex.match(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
        
    # Check duplicate email
    result = await db.execute(select(models.User).filter_by(email=user.email))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
        
    hashed = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    response.headers['Location'] = f'/api/v1/auth/register/'
    return db_user

# DOCUMENTATION: OAuth2 Authorization Code Flow vs Simple JWT Login
#
# 1. OAuth2 Authorization Code Flow:
#    - Intended for third-party client integrations. The client application redirects the user
#      to an authorization server where they log in and grant permissions.
#    - The authorization server redirects back to the client with a temporary "Authorization Code".
#    - The client then exchanges this code with the authorization server for an "Access Token".
#    - Benefits: The client never sees the user's password, and access can be restricted by scopes.
#
# 2. Simple JWT Login (Resource Owner Password Credentials):
#    - Intended for first-party, trusted applications (e.g., our own SPA or mobile app).
#    - The user inputs their username/password directly into the app, which POSTs them to the backend.
#    - The backend validates the password and immediately returns a JWT token.
#    - Benefits: Simpler to implement, fewer redirects, but requires the client to handle raw passwords.

@app.post('/api/v1/auth/login/', response_model=TokenResponse, tags=["Auth"])
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter_by(email=credentials.email))
    user = result.scalars().first()
    if not user or not security.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# ==================== COURSE CRUD ====================

# POST /api/v1/courses/
@app.post('/api/v1/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=["Courses"], summary="Create a new course", response_description="The created course details")
async def create_course(
    course: CourseCreate,
    response: Response,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify that the department exists
    result = await db.execute(select(models.Department).filter_by(id=course.department_id))
    dept = result.scalars().first()
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department with id {course.department_id} does not exist."
        )
    
    # Check if a course with the same code already exists
    result = await db.execute(select(models.Course).filter_by(code=course.code))
    existing_course = result.scalars().first()
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with code '{course.code}' already exists."
        )

    db_course = models.Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id
    )
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    
    response.headers['Location'] = f'/api/v1/courses/{db_course.id}/'
    return db_course

# GET /api/v1/courses/{course_id}
@app.get('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=["Courses"])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter_by(id=course_id))
    db_course = result.scalars().first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    return db_course

# GET /api/v1/courses/
@app.get('/api/v1/courses/', response_model=CoursePaginationResponse, tags=["Courses"])
async def get_courses(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    # Discussion on API Versioning Strategies:
    # 1. URL Versioning (e.g. /api/v1/courses/):
    #    - Pros: Highly visible, straightforward to implement, can be cached by browsers/gateways out of the box.
    #    - Cons: Pollutes the URL structure; breaking changes require changing all endpoints and client integrations.
    # 2. Header-based Versioning (e.g. Accept: application/vnd.api+json;version=1):
    #    - Pros: Keeps URLs clean, adheres to REST principles (URL represents resource, header represents format).
    #    - Cons: Harder to test directly in a browser without browser extensions or code. Caching becomes more 
    #      complex since caching keys must consider headers.

    # Count total matching courses
    count_query = select(models.Course)
    if department_id is not None:
        count_query = count_query.filter_by(department_id=department_id)
    if search:
        count_query = count_query.where(
            (models.Course.name.ilike(f"%{search}%")) | 
            (models.Course.code.ilike(f"%{search}%"))
        )
    
    total_res = await db.execute(select(func.count()).select_from(count_query.subquery()))
    total = total_res.scalar()

    # Calculate offset
    offset = (page - 1) * page_size
    
    # Query database for results
    query = count_query.offset(offset).limit(page_size)
    res = await db.execute(query)
    courses = res.scalars().all()

    # Construct next and previous URLs
    url_path = f"{request.url.scheme}://{request.url.netloc}{request.url.path}"
    
    next_url = None
    if offset + page_size < total:
        next_params = dict(request.query_params)
        next_params["page"] = page + 1
        next_params["page_size"] = page_size
        next_url = f"{url_path}?{urllib.parse.urlencode(next_params)}"
        
    prev_url = None
    if page > 1:
        prev_params = dict(request.query_params)
        prev_params["page"] = page - 1
        prev_params["page_size"] = page_size
        prev_url = f"{url_path}?{urllib.parse.urlencode(prev_params)}"

    return {
        "count": total,
        "next": next_url,
        "previous": prev_url,
        "results": courses
    }

# PUT /api/v1/courses/{course_id}
@app.put('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=["Courses"])
async def update_course(course_id: int, course: CourseCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter_by(id=course_id))
    db_course = result.scalars().first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    
    # Verify that the department exists
    dept_result = await db.execute(select(models.Department).filter_by(id=course.department_id))
    dept = dept_result.scalars().first()
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department with id {course.department_id} does not exist."
        )

    # Check duplicate code if code has changed
    if course.code != db_course.code:
        code_result = await db.execute(select(models.Course).filter_by(code=course.code))
        existing_course = code_result.scalars().first()
        if existing_course and existing_course.id != course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course with code '{course.code}' already exists."
            )

    db_course.name = course.name
    db_course.code = course.code
    db_course.credits = course.credits
    db_course.department_id = course.department_id
        
    await db.commit()
    await db.refresh(db_course)
    return db_course

# PATCH /api/v1/courses/{course_id}
@app.patch('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=["Courses"])
async def patch_course(course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter_by(id=course_id))
    db_course = result.scalars().first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    
    if hasattr(course, "model_dump"):
        update_data = course.model_dump(exclude_unset=True)
    else:
        update_data = course.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == "department_id":
            dept_result = await db.execute(select(models.Department).filter_by(id=value))
            dept = dept_result.scalars().first()
            if not dept:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Department with id {value} does not exist."
                )
        if key == "code" and value != db_course.code:
            code_result = await db.execute(select(models.Course).filter_by(code=value))
            existing_course = code_result.scalars().first()
            if existing_course and existing_course.id != course_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course with code '{value}' already exists."
                )
        setattr(db_course, key, value)
        
    await db.commit()
    await db.refresh(db_course)
    return db_course

# DELETE /api/v1/courses/{course_id}
@app.delete('/api/v1/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
async def delete_course(
    course_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Course).filter_by(id=course_id))
    db_course = result.scalars().first()
    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    await db.delete(db_course)
    await db.commit()
    return None

# ==================== DEPARTMENT CRUD ====================

# GET /api/v1/departments/{department_id}
@app.get('/api/v1/departments/{department_id}', response_model=DepartmentResponse, tags=["Departments"])
async def get_department(department_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Department).filter_by(id=department_id))
    db_dept = result.scalars().first()
    if not db_dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Department not found'
        )
    return db_dept


# ==================== STUDENT CRUD ====================

# POST /api/v1/students/
@app.post('/api/v1/students/', response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
async def create_student(student: StudentCreate, response: Response, db: AsyncSession = Depends(get_db)):
    # Check if a student with the same email already exists
    result = await db.execute(select(models.Student).filter_by(email=student.email))
    existing_student = result.scalars().first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with email '{student.email}' already exists."
        )

    db_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email
    )
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    
    response.headers['Location'] = f'/api/v1/students/{db_student.id}/'
    return db_student

# GET /api/v1/students/{student_id}
@app.get('/api/v1/students/{student_id}', response_model=StudentResponse, tags=["Students"])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter_by(id=student_id))
    db_student = result.scalars().first()
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Student not found'
        )
    return db_student

# GET /api/v1/students/
@app.get('/api/v1/students/', response_model=List[StudentResponse], tags=["Students"])
async def get_students(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Student).offset(skip).limit(limit)
    result = await db.execute(query)
    students = result.scalars().all()
    return students

# PUT /api/v1/students/{student_id}
@app.put('/api/v1/students/{student_id}', response_model=StudentResponse, tags=["Students"])
async def update_student(student_id: int, student: StudentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter_by(id=student_id))
    db_student = result.scalars().first()
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Student not found'
        )
    
    if hasattr(student, "model_dump"):
        update_data = student.model_dump(exclude_unset=True)
    else:
        update_data = student.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == "email":
            # Check if email is already taken by another student
            email_result = await db.execute(select(models.Student).filter_by(email=value))
            existing = email_result.scalars().first()
            if existing and existing.id != student_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Student with email '{value}' already exists."
                )
        setattr(db_student, key, value)
        
    await db.commit()
    await db.refresh(db_student)
    return db_student

# DELETE /api/v1/students/{student_id}
@app.delete('/api/v1/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter_by(id=student_id))
    db_student = result.scalars().first()
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Student not found'
        )
    await db.delete(db_student)
    await db.commit()
    return None


# ==================== ENROLLMENT CRUD ====================

def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}", flush=True)

# POST /api/v1/enrollments/
@app.post('/api/v1/enrollments/', response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED, tags=["Enrollments"])
async def create_enrollment(
    enrollment: EnrollmentCreate,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # Verify student exists
    student_result = await db.execute(select(models.Student).filter_by(id=enrollment.student_id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with id {enrollment.student_id} does not exist."
        )

    # Verify course exists
    course_result = await db.execute(select(models.Course).filter_by(id=enrollment.course_id))
    course = course_result.scalars().first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with id {enrollment.course_id} does not exist."
        )

    # Check if student is already enrolled in this course
    enrollment_result = await db.execute(
        select(models.Enrollment).filter_by(
            student_id=enrollment.student_id,
            course_id=enrollment.course_id
        )
    )
    existing_enrollment = enrollment_result.scalars().first()
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course."
        )

    db_enrollment = models.Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    )
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)

    # Trigger background task for email confirmation
    background_tasks.add_task(send_confirmation_email, student.email)

    response.headers['Location'] = f'/api/v1/enrollments/{db_enrollment.id}/'
    return db_enrollment

# GET /api/v1/enrollments/{enrollment_id}
@app.get('/api/v1/enrollments/{enrollment_id}', response_model=EnrollmentResponse, tags=["Enrollments"])
async def get_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).filter_by(id=enrollment_id))
    db_enrollment = result.scalars().first()
    if not db_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Enrollment not found'
        )
    return db_enrollment

# GET /api/v1/enrollments/
@app.get('/api/v1/enrollments/', response_model=List[EnrollmentResponse], tags=["Enrollments"])
async def get_enrollments(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Enrollment).offset(skip).limit(limit)
    result = await db.execute(query)
    enrollments = result.scalars().all()
    return enrollments

# PUT /api/v1/enrollments/{enrollment_id}
@app.put('/api/v1/enrollments/{enrollment_id}', response_model=EnrollmentResponse, tags=["Enrollments"])
async def update_enrollment(enrollment_id: int, enrollment: EnrollmentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).filter_by(id=enrollment_id))
    db_enrollment = result.scalars().first()
    if not db_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Enrollment not found'
        )
    
    if hasattr(enrollment, "model_dump"):
        update_data = enrollment.model_dump(exclude_unset=True)
    else:
        update_data = enrollment.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == "student_id":
            # Check student exists
            student_result = await db.execute(select(models.Student).filter_by(id=value))
            if not student_result.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Student with id {value} does not exist."
                )
        if key == "course_id":
            # Check course exists
            course_result = await db.execute(select(models.Course).filter_by(id=value))
            if not course_result.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course with id {value} does not exist."
                )
        setattr(db_enrollment, key, value)
        
    await db.commit()
    await db.refresh(db_enrollment)
    return db_enrollment

# DELETE /api/v1/enrollments/{enrollment_id}
@app.delete('/api/v1/enrollments/{enrollment_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Enrollments"])
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).filter_by(id=enrollment_id))
    db_enrollment = result.scalars().first()
    if not db_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Enrollment not found'
        )
    await db.delete(db_enrollment)
    await db.commit()
    return None


# ==================== JOIN QUERY ENDPOINT ====================

# GET /api/v1/courses/{course_id}/students/
@app.get('/api/v1/courses/{course_id}/students/', response_model=List[StudentResponse], tags=["Courses", "Students"])
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    # Verify course exists
    course_result = await db.execute(select(models.Course).filter_by(id=course_id))
    course = course_result.scalars().first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Course not found'
        )
    
    # Query enrolled students
    query = select(models.Student).join(
        models.Enrollment,
        models.Student.id == models.Enrollment.student_id
    ).where(models.Enrollment.course_id == course_id)
    
    result = await db.execute(query)
    students = result.scalars().all()
    return students

