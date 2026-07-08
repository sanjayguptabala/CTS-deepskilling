from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Numeric, TIMESTAMP, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from urllib.parse import quote_plus

pwd = quote_plus("Gopal@12345")
url = f"mysql+mysqlconnector://root:{pwd}@localhost:3306/college_db"
engine = create_engine(url)

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(100), nullable=False)
    head_of_dept = Column(String(100))
    budget = Column(Numeric(12, 2))
    
    students = relationship("Student", back_populates="department")
    courses = relationship("Course", back_populates="department")

class Student(Base):
    __tablename__ = 'students'
    
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(Date)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    enrollment_year = Column(Integer)
    phone_number = Column(String(11))
    
    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = 'courses'
    
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(150), nullable=False)
    course_code = Column(String(20), unique=True)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    
    department = relationship("Department", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")

class Professor(Base):
    __tablename__ = 'professors'
    
    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id'))

class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    enrollment_date = Column(Date)
    grade = Column(String(2))
    
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class DepartmentTransferLog(Base):
    __tablename__ = 'department_transfer_log'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer)
    old_department_id = Column(Integer)
    new_department_id = Column(Integer)
    transfer_date = Column(TIMESTAMP, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer)
    course_code = Column(String(20))
    semester = Column(String(20))
    rating = Column(Integer)
    comments = Column(String(500))
    tags = Column(JSON)          
    needs_review = Column(String(10), default=None)

if __name__ == "__main__":
    Base.metadata.create_all(engine)