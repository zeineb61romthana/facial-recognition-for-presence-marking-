from datetime import datetime
import psycopg2

def fetch_employees(cursor):
    cursor.execute("SELECT id, name, photo FROM employees")
    return cursor.fetchall()

def mark_attendance(cursor, conn, employee_id, action):
    cursor.execute(
        "INSERT INTO attendance (employee_id, action) VALUES (%s, %s) RETURNING timestamp",
        (employee_id, action)
    )
    timestamp = cursor.fetchone()[0]
    conn.commit()
    print(f"{action.capitalize()} marked for employee ID {employee_id} at {timestamp}")
    return timestamp

def calculate_working_hours(cursor, conn):
    cursor.execute("""
        SELECT employee_id, DATE(timestamp) as date, 
               MIN(CASE WHEN action = 'check_in' THEN timestamp END) as first_check_in,
               MAX(CASE WHEN action = 'check_out' THEN timestamp END) as last_check_out
        FROM attendance
        WHERE DATE(timestamp) = CURRENT_DATE
        GROUP BY employee_id, DATE(timestamp)
    """)
    records = cursor.fetchall()
    
    for record in records:
        employee_id, date, first_check_in, last_check_out = record
        if first_check_in and last_check_out:
            working_hours = (last_check_out - first_check_in).total_seconds() / 3600
            cursor.execute("""
                INSERT INTO working_hours (employee_id, date, hours_worked)
                VALUES (%s, %s, %s)
                ON CONFLICT (employee_id, date) DO UPDATE
                SET hours_worked = EXCLUDED.hours_worked
            """, (employee_id, date, working_hours))
            conn.commit()
            print(f"Working hours recorded for employee ID {employee_id}: {working_hours:.2f} hours")
