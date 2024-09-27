import cv2
import numpy as np
import face_recognition
import psycopg2
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from helper_functions import fetch_employees, mark_attendance, calculate_working_hours

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Facial Recognition Attendance System")
        self.root.geometry("800x600")
        self.setup_ui()
        self.db_conn = self.connect_db()
        self.db_cursor = self.db_conn.cursor()
        self.employees = self.fetch_employees()
        self.known_encodings = [face_recognition.face_encodings(cv2.imdecode(np.frombuffer(emp[2], np.uint8), cv2.IMREAD_COLOR))[0] for emp in self.employees]
        self.known_ids = [emp[0] for emp in self.employees]
        self.cap = cv2.VideoCapture(0)
        self.action = None  # Initialize action to None
        self.current_employee_id = None
        self.current_employee_name = None
        self.current_alert = None  # To keep track of the current alert message
        self.update_frame()

    def connect_db(self):
        return psycopg2.connect(
            dbname="attendance_system",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )

    def fetch_employees(self):
        return fetch_employees(self.db_cursor)

    def setup_ui(self):
        # Create frames
        self.home_frame = tk.Frame(self.root)
        self.attendance_frame = tk.Frame(self.root)

        # Setup home frame
        self.logo_image = Image.open("photos/logo.png")  # Update this path if necessary
        self.logo_image = self.logo_image.resize((200, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = tk.Label(self.home_frame, image=self.logo_photo)
        self.logo_label.pack(pady=20)

        self.welcome_label = tk.Label(self.home_frame, text="Welcome to ProoSoft Cloud Company", font=("Helvetica", 20, "bold"), fg="#004d99")
        self.welcome_label.pack(pady=10)

        self.contact_info = tk.Label(self.home_frame, text="Centre Urbain Nord Carthage Palace Tunis 1003 Tunisia\n+216 70 033 027\ninfo@proosoft.com", font=("Helvetica", 14), justify=tk.CENTER)
        self.contact_info.pack(pady=10)

        self.enter_button = ttk.Button(self.home_frame, text="Enter Attendance System", command=self.show_attendance_frame, style="TButton")
        self.enter_button.pack(pady=20)

        self.home_frame.pack(fill="both", expand=True)

        # Setup attendance frame
        self.greeting_label = tk.Label(self.attendance_frame, text="Welcome", font=("Helvetica", 16, "bold"), fg="#004d99")
        self.greeting_label.pack(pady=10)

        self.video_label = tk.Label(self.attendance_frame)
        self.video_label.pack()

        self.attendance_info_label = tk.Label(self.attendance_frame, text="", font=("Helvetica", 12))
        self.attendance_info_label.pack(pady=10)

        self.message_label = tk.Label(self.attendance_frame, text="", font=("Helvetica", 12))
        self.message_label.pack(pady=10)

        self.total_hours_label = tk.Label(self.attendance_frame, text="", font=("Helvetica", 12))
        self.total_hours_label.pack(pady=10)

        self.check_in_button = ttk.Button(self.attendance_frame, text="Check In", command=self.mark_check_in, style="TButton")
        self.check_in_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.check_out_button = ttk.Button(self.attendance_frame, text="Check Out", command=self.mark_check_out, style="TButton")
        self.check_out_button.pack(side=tk.RIGHT, padx=20, pady=20)

        self.alert_label = tk.Label(self.attendance_frame, text="", font=("Helvetica", 12, "bold"), fg="red")
        self.alert_label.pack(pady=10)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)

    def show_attendance_frame(self):
        self.home_frame.pack_forget()
        self.attendance_frame.pack(fill="both", expand=True)

    def mark_check_in(self):
        self.action = "check_in"
        self.message_label.config(text="You'll do a great job!")
        self.mark_attendance()

    def mark_check_out(self):
        self.action = "check_out"
        self.message_label.config(text="Thank you for your good work today")
        self.mark_attendance()

    def get_greeting(self, name):
        current_hour = datetime.now().hour
        if current_hour < 12:
            return f"Good Morning, {name}!"
        elif current_hour < 18:
            return f"Good Afternoon, {name}!"
        else:
            return f"Good Evening, {name}!"

    def mark_attendance(self):
        if self.current_employee_id is not None and self.action is not None:
            timestamp = mark_attendance(self.db_cursor, self.db_conn, self.current_employee_id, self.action)
            greeting_text = self.get_greeting(self.current_employee_name)
            self.greeting_label.config(text=greeting_text)
            self.attendance_info_label.config(text=f"{self.action.capitalize()} at: {timestamp.strftime('%H:%M:%S')}")
            if self.action == "check_out":
                self.update_working_hours(self.current_employee_id)
            self.action = None

    def update_frame(self):
        success, img = self.cap.read()
        if not success:
            self.show_alert("Open your camera please!")
            self.root.after(1000, self.update_frame)
            return

        imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faces_cur_frame = face_recognition.face_locations(imgS)
        encodes_cur_frame = face_recognition.face_encodings(imgS, faces_cur_frame)

        if len(faces_cur_frame) == 0:
            self.show_alert("No face detected. Please appear in front of the camera.")
            self.root.after(1000, self.update_frame)
            return

        recognized = False
        for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
            matches = face_recognition.compare_faces(self.known_encodings, encode_face)
            face_dis = face_recognition.face_distance(self.known_encodings, encode_face)
            match_index = np.argmin(face_dis)

            if matches[match_index] and face_dis[match_index] < 0.50:
                recognized = True
                self.current_employee_id = self.known_ids[match_index]
                self.current_employee_name = self.employees[match_index][1]
                greeting_text = self.get_greeting(self.current_employee_name)
                self.greeting_label.config(text=greeting_text)
                self.message_label.config(text="Face detected. Please press Check In or Check Out.")
                self.check_in_button.state(["!disabled"])
                self.check_out_button.state(["!disabled"])
                self.clear_alert()  # Clear the alert if a face is recognized

                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, self.current_employee_name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                break

        if not recognized:
            self.show_alert("This person does not work at ProoSoft Cloud Company.")
            self.current_employee_id = None
            self.current_employee_name = None
            self.check_in_button.state(["disabled"])
            self.check_out_button.state(["disabled"])

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def update_working_hours(self, employee_id):
        self.db_cursor.execute("""
            SELECT 
                MIN(CASE WHEN action = 'check_in' THEN timestamp END) as first_check_in,
                MAX(CASE WHEN action = 'check_out' THEN timestamp END) as last_check_out
            FROM attendance
            WHERE employee_id = %s AND DATE(timestamp) = CURRENT_DATE
            GROUP BY employee_id
        """, (employee_id,))
        record = self.db_cursor.fetchone()
        if record:
            first_check_in, last_check_out = record
            if first_check_in and last_check_out:
                working_seconds = (last_check_out - first_check_in).total_seconds()
                hours, remainder = divmod(working_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.total_hours_label.config(text=f"Total Working Hours: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
            else:
                self.total_hours_label.config(text="Total Working Hours: Not yet available")

    def show_alert(self, message):
        if self.current_alert != message:
            self.alert_label.config(text=message)
            self.current_alert = message

    def clear_alert(self):
        self.alert_label.config(text="")
        self.current_alert = None

    def __del__(self):
        self.cap.release()
        self.db_cursor.close()
        self.db_conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()
