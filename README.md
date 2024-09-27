# 📸 Facial Recognition Attendance System for ProoSoft Cloud Company

Welcome to the **Facial Recognition Attendance System**, a modern solution designed to streamline employee attendance tracking with facial recognition technology. Developed for **ProoSoft Cloud Company**, this application ensures accurate and efficient attendance management, minimizing manual processes and enhancing productivity.

## ✨ Features
- **Real-time Facial Recognition**: Utilizes OpenCV and `face_recognition` to accurately identify employees.
- **Attendance Marking**: Easily record **Check-In** and **Check-Out** times using intuitive buttons.
- **Employee Database Integration**: Stores attendance data in a PostgreSQL database for easy access and report generation.
- **Tkinter User Interface**: Simple and interactive UI for better user experience.
- **Working Hours Calculation**: Automatically computes daily working hours and updates the records.

## 🛠️ Tech Stack
- **Programming Language**: Python
- **Libraries**: OpenCV, NumPy, `face_recognition`, Tkinter
- **Database**: PostgreSQL
- **Image Handling**: PIL (Pillow)

## 🚀 How It Works
1. **Employee Data Management**: Fetch employee details, including facial images, from the PostgreSQL database.
2. **Face Recognition**: Use a webcam to capture and recognize employees in real-time.
3. **Attendance Logging**: Employees can **Check-In** or **Check-Out** with a click, and the timestamp is stored in the database.
4. **Working Hours Calculation**: Automatically calculates and displays total working hours at the end of the day.

## 📂 Folder Structure
- **`main.py`**: Main script containing the user interface and facial recognition logic.
- **`helper_functions.py`**: Helper functions for fetching employee data, marking attendance, and calculating working hours.
- **`photos/`**: Contains logo and other image assets.

## 🔧 Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/zeineb61romthana/acial-recognition-for-presence-marking-.git
    ```
2. Install the required Python packages:
    ```bash
    pip install opencv-python-headless face_recognition psycopg2 Pillow
    ```
3. Run the application:
    ```bash
    python GUI.py
    ```
