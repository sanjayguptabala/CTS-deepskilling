from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # Relationship to nested Course models
    courses = relationship('Course', back_populates='department', cascade='all, delete-orphan', lazy='selectin')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, index=True, nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)

    # Relationship to Department
    department = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course', cascade='all, delete-orphan', lazy='selectin')

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)

    # Relationship to Enrollments
    enrollments = relationship('Enrollment', back_populates='student', cascade='all, delete-orphan', lazy='selectin')

class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    # Relationships
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)

