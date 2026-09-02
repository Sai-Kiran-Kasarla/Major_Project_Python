# 🎓 LearnHub - Learning Management System

## 📌 Project Overview

**LearnHub** is a Python-based **Learning Management System (LMS)** designed to provide an interactive platform for managing online learning activities.

The system supports three main user roles:

- 👨‍💼 Administrator
- 👨‍🏫 Instructor
- 👨‍🎓 Student

Each role has its own dashboard and permissions.

The application is developed using **Python and Streamlit**, with **Excel (`lms_data.xlsx`)** used for data storage and management.

---

# 🎯 Project Objectives

The main objectives of LearnHub are:

- Provide a centralized learning platform.
- Manage students and instructors.
- Allow instructors to create and manage courses.
- Allow students to enroll in courses.
- Manage modules and learning materials.
- Manage assignments and examinations.
- Track attendance.
- Track student progress.
- Analyze student performance.
- Provide dashboards and statistics.
- Generate course completion certificates.
- Provide role-based access to different users.

---

# ✨ Key Features

## 👨‍💼 Administrator

The administrator can:

- Login securely.
- View the admin dashboard.
- Manage students.
- Manage instructors.
- Approve instructor registrations.
- Create courses.
- Assign instructors to courses.
- View platform statistics.
- View course statistics.
- View student statistics.
- View instructor statistics.
- Monitor overall platform performance.

---

## 👨‍🏫 Instructor

The instructor can:

- Register as an instructor.
- Login after administrator approval.
- View assigned courses.
- Manage course content.
- Add modules.
- Add module descriptions.
- Add module links.
- Add tasks.
- Create assignments.
- Manage assignment marks.
- Create exams.
- Add exam questions.
- Record student attendance.
- View student performance.
- View student progress.
- Complete/mark courses as completed for students.

---

## 👨‍🎓 Student

The student can:

- Register.
- Login.
- View available courses.
- Request course enrollment.
- View enrolled courses.
- Access course modules.
- Access learning materials.
- View assignments.
- Take examinations.
- View exam results.
- View attendance.
- Track course progress.
- View performance.
- View completed courses.
- View course completion certificates.

---

# 🏗️ Project Architecture

The project follows a modular structure.

```text
LearnHub/
│
├── main.py
├── lms.py
├── model.py
├── mail_services.py
├── question_bank.py
├── lms_data.xlsx
├── requirements.txt
├── README.md
└── .gitignore
