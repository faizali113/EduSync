# EduSync - Project Walkthrough

## 1. Project Overview
**EduSync** is a multi-role School Management System built with **Django**. It allows an "Institution" (Admin) to sign up and manage their entire school ecosystem, including teachers, students, courses, and grades.

Key Philosophy: **"One Platform, Three Views"**
- **Institution Admin**: Has full control (GOD mode for their school).
- **Teachers**: Can view their assigned classes and students.
- **Students**: Can view their grades and profile.

---

## 2. Architecture (The "Apps")
The project is split into modular Django apps:

1.  **`accounts`**: Handles the main "Institution" Signup/Login and the Landing page.
2.  **`institution`**: The core dashboard. Manages the school profile and global announcements (CMS).
3.  **`teacher`**: Manages faculty records. Auto-generates user accounts for teachers.
4.  **`student`**: Manages student records. Auto-generates user accounts for students.
5.  **`academics`**: Handles Courses/Subjects and Grades/Marks.

---

## 3. The "Secret Sauce" (Key Workflows)

### A. The "Smart" Authentication
We don't just have a simple login. We have a **Role-Based Authentication** system.
- **Main Login**: For Institution Admins (using Email/Password).
- **Portal Login**: For Teachers & Students.
    - Instead of registering themselves, the Admin creates them.
    - They login using a special simplified form (Name + ID).
    - Code: `institution/views.py` -> `_handle_portal_login`. It verifies the name matches the ID and logs them in manually.

### B. Auto-User Generation
When an Admin adds a Student or Teacher, we don't just add a database row. We **automatically create a Django User Account** for them.
- **File**: `student/views.py` (inside `student_create`)
- **Logic**: 
    1. Admin fills out a form (Name: "John Doe", Roll No: "101").
    2. System creates a Django `User` (Username: `student_101`, Password: `101`).
    3. System links this User to a `Student` profile.
    4. This allows John Doe to log in immediately without setting up an account.

### C. The Dashboard Router
We have a smart traffic controller at `/institution/dashboard/`.
- **File**: `institution/views.py` -> `dashboard_view`
- **Logic**:
    - If a **Student** tries to access the Admin panel, they are kicked to the *Student Dashboard*.
    - If a **Teacher** tries, they go to the *Teacher Dashboard*.
    - Only the **Admin** sees the control panel.

---

## 4. Key Code Files to Show
If you're walking them through the code, open these files in order:

1.  **`accounts/models.py`**: Show the `UserProfile` class. This is where we define the `ROLE_CHOICES` (Admin, Teacher, Student).
2.  **`institution/views.py`**: Show the `dashboard_view`. It's the "Main Menu" of the app.
3.  **`templates/base.html`**: The main layout. Show how we use Django Template Language (`{% if user.is_authenticated %}`) to change the navbar dynamically.

## 5. Technical Stack
- **Backend**: Python / Django 5.0
- **Database**: SQLite (Development)
- **Frontend**: HTML5, Bootstrap 5 (for layout), CSS Variables (for theming).
- **Security**: Django's built-in CSRF protection and `@login_required` decorators are used everywhere.
