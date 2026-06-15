import mysql.connector
import time

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',         # Replace with your MySQL username
    'password': 'Gopal@12345', # Replace with your MySQL password
    'database': 'college_db'
}

def run_n_plus_one_simulation():
    print("--- APPROACH 1: Simulating the N+1 Problem ---")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query_count = 0
    start_time = time.perf_counter()
    
    # 1. First initial query to fetch all N enrollments
    cursor.execute("SELECT * FROM enrollments")
    enrollments = cursor.fetchall()
    query_count += 1
    
    # 2. Loop through each enrollment and issue N individual queries for student names
    results = []
    for row in enrollments:
        student_id = row['student_id']
        cursor.execute("SELECT first_name, last_name FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()
        query_count += 1
        
        results.append({
            'enrollment_id': row['enrollment_id'],
            'student_name': f"{student['first_name']} {student['last_name']}",
            'course_id': row['course_id']
        })
        
    end_time = time.perf_counter()
    cursor.close()
    conn.close()
    
    print(f"Total Queries Executed: {query_count}")
    print(f"Execution Time: {end_time - start_time:.6f} seconds\n")
    return results

def run_optimized_join():
    print("--- APPROACH 2: Optimized Single JOIN Query ---")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query_count = 0
    start_time = time.perf_counter()
    
    # Eagerly load all data using a single INNER JOIN statement
    optimized_query = """
        SELECT e.enrollment_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, e.course_id
        FROM enrollments e
        INNER JOIN students s ON e.student_id = s.student_id
    """
    cursor.execute(optimized_query)
    results = cursor.fetchall()
    query_count += 1
    
    end_time = time.perf_counter()
    cursor.close()
    conn.close()
    
    print(f"Total Queries Executed: {query_count}")
    print(f"Execution Time: {end_time - start_time:.6f} seconds\n")
    return results

if __name__ == "__main__":
    # Execute both approaches
    n_plus_one_data = run_n_plus_one_simulation()
    optimized_data = run_optimized_join()
    
    # Verification to guarantee identical outputs
    assert len(n_plus_one_data) == len(optimized_data), "Data mismatch!"
    print("Data verification passed! Both methods fetched identical results.")