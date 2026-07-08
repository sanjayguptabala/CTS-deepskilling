from sqlalchemy import func, select, text
from sqlalchemy.orm import sessionmaker
from models import engine, Feedback

Session = sessionmaker(bind=engine)
session = Session()
# 71 & 72. Filters semester, groups by course, rounds average rating to 1 decimal place, and sorts descending
pipeline1 = (
    session.query(
        Feedback.course_code.label("course_code"),
        func.count(Feedback.id).label("total_feedback"),
        func.round(func.avg(Feedback.rating), 1).label("average_rating")
    )
    .filter(Feedback.semester == '2022-ODD')
    .group_by(Feedback.course_code)
    .order_by(text("average_rating DESC"))
    .all()
)

print("--- Steps 71 & 72: Course Aggregation Report ---")
for row in pipeline1:
    print(f"Course: {row.course_code} | Total Feedback: {row.total_feedback} | Avg Rating: {row.average_rating}")
# 73. Uses MySQL JSON_TABLE to unwind the JSON array entries into separate relational rows
unwind_query = text("""
    SELECT jt.tag_name AS tag, COUNT(*) AS count
    FROM feedback,
    JSON_TABLE(feedback.tags, '$[*]' COLUMNS(tag_name VARCHAR(100) PATH '$')) jt
    GROUP BY jt.tag_name
    ORDER BY count DESC;
""")

pipeline3 = session.execute(unwind_query).fetchall()

print("\n--- Step 73: Tag Frequency Leaderboard ---")
for row in pipeline3:
    print(f"Tag: {row.tag:<15} | Frequency Count: {row.count}")

# 74. Optimization: Add a MySQL Index and Verify Execution Path

try:
    session.execute(text("CREATE INDEX idx_course_code ON feedback(course_code);"))
    session.commit()
    print("\n--- Step 74: Index created successfully ---")
except Exception as e:
    print("\n--- Step 74: Index verification check ---")

# Run EXPLAIN statement to show execution stats layout
explain_query = text("EXPLAIN SELECT * FROM feedback WHERE course_code = 'CS101';")
explain_results = session.execute(explain_query).fetchall()

# Print the keys and rows directly to avoid the attribute mapping error
print("MySQL EXPLAIN Row Output (Look for index/ref mappings):")
for row in explain_results:
    print(list(row))  # Prints the row cleanly as a list of column values

session.close()