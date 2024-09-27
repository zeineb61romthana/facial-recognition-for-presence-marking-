#add_employees.py
import psycopg2

def add_employee(name, photo_path):
    with open(photo_path, 'rb') as f:
        photo = f.read()

    with psycopg2.connect(
        dbname="attendance_system",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM employees WHERE name = %s", (name,))
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO employees (name, photo) VALUES (%s, %s)",
                    (name, photo)
                )
                conn.commit()
                print(f"Employee {name} added successfully.")
            else:
                print(f"Employee {name} already exists in the database.")

if __name__ == "__main__":
    add_employee('Zeineb', 'C:\\Users\\me\\OneDrive\\Bureau\\FR\\employee_photos\\ZEINEB.jpeg')
    add_employee('eya', 'C:\\Users\\me\\OneDrive\\Bureau\\FR\\employee_photos\\eya.jpg')
    add_employee('rania', 'C:\\Users\\me\\OneDrive\\Bureau\\FR\\employee_photos\\rania.jpg')
