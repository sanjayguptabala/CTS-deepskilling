from app import create_app
from extensions import db
from courses.models import Department, Course

app = create_app()
with app.app_context():
    # Clear existing entries
    db.session.query(Course).delete()
    db.session.query(Department).delete()
    db.session.commit()
    
    # 1. Insert 2 departments
    cs = Department(name="Computer Science", head_of_dept="Dr. Alan Turing", budget=110000.00)
    math = Department(name="Mathematics", head_of_dept="Dr. Emmy Noether", budget=88000.00)
    db.session.add(cs)
    db.session.add(math)
    db.session.commit()
    print("Inserted Departments:")
    print(f"- {cs}")
    print(f"- {math}")
    
    # 2. Insert 3 courses
    c1 = Course(name="Introduction to Programming", code="CS101", credits=4, department=cs)
    c2 = Course(name="Algorithms and Data Structures", code="CS201", credits=4, department=cs)
    c3 = Course(name="Calculus I", code="MATH101", credits=3, department=math)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.commit()
    
    # 3. Query all courses to verify
    all_courses = db.session.query(Course).all()
    print(f"\nAll courses retrieved via ORM (Count: {len(all_courses)}):")
    for course in all_courses:
        print(f"- ID: {course.id} | Name: {course.name} | Code: {course.code} | Dept: {course.department.name}")
