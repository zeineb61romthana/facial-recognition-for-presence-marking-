# setup_database.py
import psycopg2

def create_tables():
    with psycopg2.connect(
        dbname="attendance_system",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS attendance CASCADE")
            cursor.execute("DROP TABLE IF EXISTS working_hours CASCADE")
            cursor.execute("DROP TABLE IF EXISTS employees CASCADE")

            cursor.execute("""
                CREATE TABLE employees (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    photo BYTEA
                )
            """)
            cursor.execute("""
                CREATE TABLE attendance (
                    id SERIAL PRIMARY KEY,
                    employee_id INTEGER REFERENCES employees(id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    action VARCHAR(10) NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE working_hours (
                    id SERIAL PRIMARY KEY,
                    employee_id INTEGER REFERENCES employees(id),
                    date DATE NOT NULL,
                    hours_worked DECIMAL(5, 2) NOT NULL
                )
            """)
            conn.commit()

if __name__ == "__main__":
    create_tables()
