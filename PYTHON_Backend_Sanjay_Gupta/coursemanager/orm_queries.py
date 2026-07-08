# orm_queries.py
# ==============================================================================
# Django ORM CRUD & Complex Queries Script
# ==============================================================================

from django.db import connection, reset_queries
from django.db.models import Count, F
from courses.models import Department, Course, Student, Enrollment

# Step 16: Create objects using Model.objects.create(...)
print("=== Step 16: Populating database ===")

# Clear previous entries to prevent duplicate key errors and start fresh
Enrollment.objects.all().delete()
Student.objects.all().delete()
Course.objects.all().delete()
Department.objects.all().delete()

# Create 2 Departments
cs = Department.objects.create(name="Computer Science", head_of_dept="Dr. Alan Turing", budget=100000.00)
math = Department.objects.create(name="Mathematics", head_of_dept="Dr. Emmy Noether", budget=80000.00)
print(f"Created Departments:\n- {cs} (Budget: ${cs.budget})\n- {math} (Budget: ${math.budget})")

# Create 4 Courses
c1 = Course.objects.create(name="Introduction to Programming", code="CS101", credits=4, department=cs)
c2 = Course.objects.create(name="Algorithms and Data Structures", code="CS201", credits=4, department=cs)
c3 = Course.objects.create(name="Calculus I", code="MATH101", credits=3, department=math)
c4 = Course.objects.create(name="Linear Algebra", code="MATH201", credits=3, department=math)
print(f"\nCreated Courses:\n- {c1} ({c1.code})\n- {c2} ({c2.code})\n- {c3} ({c3.code})\n- {c4} ({c4.code})")

# Create 5 Students
s1 = Student.objects.create(first_name="Alice", last_name="Smith", email="alice@example.com", department=cs, enrollment_year=2025)
s2 = Student.objects.create(first_name="Bob", last_name="Jones", email="bob@example.com", department=cs, enrollment_year=2025)
s3 = Student.objects.create(first_name="Charlie", last_name="Brown", email="charlie@example.com", department=math, enrollment_year=2026)
s4 = Student.objects.create(first_name="Diana", last_name="Prince", email="diana@example.com", department=cs, enrollment_year=2024)
s5 = Student.objects.create(first_name="Evan", last_name="Wright", email="evan@example.com", department=math, enrollment_year=2026)
print(f"\nCreated Students:\n- {s1}\n- {s2}\n- {s3}\n- {s4}\n- {s5}")


# Step 17: Query all courses in a specific department (Foreign Key span lookup)
print("\n=== Step 17: Query courses in Computer Science (ForeignKey lookup) ===")
cs_courses = Course.objects.filter(department__name='Computer Science')
print("Courses in 'Computer Science' department:")
for course in cs_courses:
    print(f"- {course.name} ({course.code})")


# Step 18: values() and annotate() to count the number of courses per department
print("\n=== Step 18: Annotate course count per department ===")
departments_with_counts = Department.objects.annotate(course_count=Count('course'))
for dept in departments_with_counts:
    print(f"Department: {dept.name} | Course Count: {dept.course_count}")


# Step 19: select_related to fetch all students along with department in a single query
print("\n=== Step 19: Fetching students with select_related ===")
reset_queries()

# Let's run query WITH select_related
students_with_dept = list(Student.objects.select_related('department'))
print("Students with their department (using select_related):")
for student in students_with_dept:
    print(f"- Student: {student.first_name} {student.last_name} | Department: {student.department.name}")

print(f"\nNumber of SQL queries executed: {len(connection.queries)}")
print("Executed SQL query detail:")
for idx, q in enumerate(connection.queries, 1):
    print(f"{idx}. {q['sql']}")


# Step 20: update department budget by 10% using F()
print("\n=== Step 20: Bulk budget update by +10% using F() ===")
print("Budgets BEFORE update:")
for dept in Department.objects.all():
    print(f"- {dept.name}: ${dept.budget}")

# Perform the bulk update
Department.objects.update(budget=F('budget') * 1.1)

print("\nBudgets AFTER update:")
for dept in Department.objects.all():
    print(f"- {dept.name}: ${dept.budget}")

print("\n=== Django ORM Verification Successful ===")
