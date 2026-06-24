from sqlalchemy.orm import sessionmaker
# This imports the engine connection and Feedback table table layout from your models.py
from models import engine, Feedback 

# Start the database operational communication session
Session = sessionmaker(bind=engine)
session = Session()

# --- Optional: Add baseline records so your queries have something to find ---
if session.query(Feedback).count() == 0:
    sample_feedback = [
        Feedback(student_id=1, course_code="CS101", semester="2022-ODD", rating=5, comments="Excellent!", tags=["well-structured", "good-examples"]),
        Feedback(student_id=2, course_code="CS101", semester="2022-ODD", rating=4, comments="Good but heavy.", tags=["challenging"]),
        Feedback(student_id=3, course_code="CS102", semester="2021-EVEN", rating=2, comments="Too slow.", tags=["slow-paced"]),
        Feedback(student_id=4, course_code="CS101", semester="2022-ODD", rating=2, comments="Hard to follow.", tags=["challenging", "heavy-load"])
    ]
    session.add_all(sample_feedback)
    session.commit()

# 65. READ: Find all feedback documents where rating is 5

r65 = session.query(Feedback).filter(Feedback.rating == 5).all()
print("--- Step 65: Rating is 5 ---")
for f in r65:
    print(f"ID: {f.id} | Course: {f.course_code} | Rating: {f.rating}")


# 66. READ: Find feedback for course CS101 where the tags array contains 'challenging'

r66 = session.query(Feedback).filter(
    Feedback.course_code == 'CS101',
    Feedback.tags.contains('challenging')
).all()
print("\n--- Step 66: CS101 with 'challenging' tag ---")
for f in r66:
    print(f"ID: {f.id} | Course: {f.course_code} | Tags: {f.tags}")


# 67. READ: Retrieve only specific projection fields

r67 = session.query(Feedback.student_id, Feedback.course_code, Feedback.rating).all()
print("\n--- Step 67: Projection Query ---")
for student_id, course_code, rating in r67:
    print(f"Student ID: {student_id} | Course: {course_code} | Rating: {rating}")


# 68. UPDATE: Add field needs_review: true for rating < 3

session.query(Feedback).filter(Feedback.rating < 3).update({"needs_review": "true"})
session.commit()
print("\n--- Step 68: Update Complete (Low ratings flagged) ---")


# 69. UPDATE: Push a new tag 'reviewed' into the tags JSON array

flagged_docs = session.query(Feedback).filter(Feedback.needs_review == "true").all()
for doc in flagged_docs:
    current_tags = list(doc.tags) if doc.tags else []
    if "reviewed" not in current_tags:
        current_tags.append("reviewed")
        doc.tags = current_tags
session.commit()
print("--- Step 69: Update Complete (Added 'reviewed' tag) ---")



# 70. DELETE: Delete all records where semester is '2021-EVEN'

deleted_count = session.query(Feedback).filter(Feedback.semester == '2021-EVEN').delete()
session.commit()
print(f"--- Step 70: Delete Complete (Removed {deleted_count} record(s)) ---")

# Close the execution line safely
session.close()