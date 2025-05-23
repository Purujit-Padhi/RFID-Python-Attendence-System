# RFID-Python-Attendence-System
This project is a smart Attendance Management System that uses RFID technology for student identification and a Python-based GUI for managing and recording attendance efficiently. Designed to streamline attendance processes in schools or colleges, it combines hardware and software for real-time tracking.

🔧 Features
🪪 RFID Integration: Uses RFID cards and Arduino to detect and identify students.

💻 Modern GUI: Built using CustomTkinter for a sleek, responsive desktop interface.

📊 Real-Time Attendance Recording: Automatically marks attendance upon RFID scan.

🧾 Excel Integration: Supports importing and exporting student data via Excel files.

⚙️ Admin Tools: Add, update, and manage student records with ease.

📡 Serial Communication: Connects with the RFID hardware via COM ports for live data.

🛠️ Tech Stack
Python (CustomTkinter for GUI, pandas for Excel handling)

Arduino UNO/Nano (with RFID module like RC522)

Serial Communication (pyserial)

Excel (xlsx/csv file support for bulk operations)

📌 Use Case
Perfect for educational institutions looking to automate and digitize their attendance system with minimal hardware.





-> Project Structure

├── (Admin) Attendence Management.py     # Admin GUI for managing classes, students, tags
├── (Run) Attendence Management.py       # Run this to start taking live attendance
├── helper.py                            # Core backend functions (add, update, extract students)
├── helper1.py                           # Attendance updater & Arduino serial communication
├── Data/
│   ├── Attendence Folder/               # Stores attendance Excel files for each class
│   └── Template/
│       ├── template.xlsx                # Base template for new class attendance files
│       ├── Db.json                      # Student database (maps RFID tag to student info)
│       └── icon.ico                     # App icon


Requirements
Python 3.8+

Required libraries:

bash
Copy
Edit
pip install customtkinter openpyxl pyserial pillow CTkMessagebox
🚀 How to Use
🔹 1. Admin Panel
Run:

bash
Copy
Edit
python "(Admin) Attendence Management.py"
🔧 Features:
Add Class – Creates a new attendance register from a template (e.g., Class_1_A.xlsx).

Add Student (Manual) – Add a student by scanning their RFID and entering details.

Add Student from File – Upload an Excel file with student Roll No and Name.

Update Student Data – Scan and edit name/class/roll number of existing students.

Change Tag ID – Reassign a different RFID tag to an existing student.

Abstract Data – View student info by scanning card.

Show Database – View/delete students from the central JSON database.

✅ All student data is stored in:

Excel file: Data/Attendence Folder/Class_X_Y.xlsx

JSON file: Data/Template/Db.json

🔹 2. Attendance Panel
Run:

bash
Copy
Edit
python "(Run) Attendence Management.py"
📌 How it works:
Select the correct COM port.

Click Connect.

Swipe RFID cards.

Attendance will be:

Marked in that day's column in the Excel sheet.

Feedback sent to LCD (e.g., “Marked Present” / “Already Punched”).

⏰ Timestamp is saved as P - 10:34:56 AM.

📂 Attendance files are saved inside:

swift
Copy
Edit
Data/Attendence Folder/
📈 Excel Format Example
Each class file (e.g., Class_1_A.xlsx) contains:

A sheet named April, May, etc.

Columns: UID, Roll No, Name, 1, 2, 3, ... (for dates)



Admin Window – Button Functionality
The Admin panel provides full control over managing classes, students, and RFID tags. Below is what each button does:

✅ 1. Add Class
📂 Creates a new class register Excel file.

Format: Class_<ClassName>_<Section>.xlsx (e.g., Class_1_A.xlsx)

Based on a pre-defined Excel template located at:
Data/Template/template.xlsx

💾 Stores new class files inside:
Data/Attendence Folder/

✅ 2. Add Student Manually
✍️ Register students one by one.

You must:

Select class from dropdown

Enter Roll Number and Student Name

Select the COM Port

Tap the RFID card on the reader

🔐 The card UID is stored and linked with the student.

✅ Data saved in both:

Db.json (student info)

Class Excel sheet (April sheet)

✅ 3. Add Student From File
📄 Upload an Excel file with student data:

pgsql
Copy
Edit
| Roll No | Name         |
|---------|--------------|
| 101     | John Smith   |
| 102     | Alice Brown  |
🧭 Navigate through the list using Next/Previous.

Tap RFID card and add them one by one.

✅ Automatically fills:

Excel attendance register

JSON database

✅ 4. Abstract Data
📖 Scan an RFID card to view the student's info.

It shows:

Name

Class

Roll Number

⚠️ No editing—just viewing.

✅ 5. Update Student Data
📝 Edit student name, class, or roll number.

Scan the RFID card → update details.

✅ Saves updates to:

JSON (Db.json)

Excel sheet (overwrites existing entry)

✅ 6. Change Tag ID
🔁 Use this to reassign a new RFID card to an existing student.

Scan new card → old UID is replaced with the new one.

✅ Updates:

JSON

Excel (changes UID column)

✅ 7. Show Database
🧾 Opens a visual list of all registered students.

Grouped by class.

Columns shown: UID, Roll No., Name

🗑️ Delete any student using the red trash icon (deletes from both JSON and Excel).

----->>>>>>>>>>>>>>>>                                   <<<<<<<<<<<<<<<<<<<<<<<<<<<<---------------------------

For any futher infor,
may contact on -> purujitpadhi@gmail.com
