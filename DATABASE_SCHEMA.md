# EduSync 2.0 - Database Schema Documentation

This document outlines the database structure for the EduSync 2.0 application. The system is built using Django and SQLite (by default), with separate applications for different modules (Academics, Accounts, Institution, Student, Teacher, Timetable).

## 1. Institution App (`institution`)
**Purpose:** Manages the core entity of the system - the School, College, or University.

### Model: `Institution`
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary Key |
| `name` | CharField | Unique name of the institution. |
| `admin` | OneToOneField (User) | Link to the Django User who is the admin. |
| `email` | EmailField | Contact email (unique). |
| `phone` | CharField | Contact number. |
| `address` | TextField | Physical address. |
| `established_year` | IntegerField | Year of establishment. |
| `created_at` | DateTimeField | Record creation timestamp. |

### Model: `News`
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary Key |
| `content` | TextField | News/Announcement text. |
| `created_at` | DateTimeField | Published date. |

---

## 2. Accounts App (`accounts`)
**Purpose:** Manages authentication, user roles, and signup workflows.

### Model: `UserProfile`
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary Key |
| `user` | OneToOneField (User) | Link to Django default User model. |
| `role` | CharField | Role: `institution_admin`, `teacher`, or `student`. |
| `phone` | CharField | User contact phone. |
| `institution` | CharField | Name of the institution (redundant for quick access). |

### Model: `SignupTable` / `LoginTable`
*Used for initial onboarding flow.*

---

## 3. Academics App (`academics`)
**Purpose:** Manages the learning structure (Courses) and performance (Grades).

### Model: `Course`
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary Key |
| `institution` | ForeignKey (Institution) | The institution offering this course. |
| `code` | CharField | Course Code (e.g., CS101). Unique per institution. |
| `name` | CharField | Course Name (e.g., Intro to Python). |
| `description` | TextField | Course details. |
| `credits` | IntegerField | Credit value (default: 3). |
| `duration_months` | PositiveIntegerField | Duration in months. |
| `department` | CharField | Department name (e.g., Science, Arts). |
| `tuition_fee` | DecimalField | Cost of the course. |
| `teachers` | ManyToManyField (Teacher) | Teachers assigned to this course. |
| `created_at` | DateTimeField | Creation timestamp. |

### Model: `Grade`
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary Key |
| `student` | ForeignKey (Student) | The student receiving the grade. |
| `course` | ForeignKey (Course) | The course graded. |
| `grade` | CharField | Letter grade (A, B, C, D, F). |
| `marks` | FloatField | Numeric score. |
| `date_assigned` | DateTimeField | When the grade was given. |

---

## 4. Teacher App (`teacher`)
**Purpose:** Manages Faculty/Staff records (HR).

### Model: `Teacher`
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary Key |
| `user` | OneToOneField (User) | Link to Django User (Authentication). |
| `institution` | ForeignKey (Institution) | Employer institution. |
| `employee_id` | CharField | Unique Employee ID. |
| `department` | CharField | Faculty Department. |
| `qualification` | CharField | Degrees/Certifications. |
| `gender` | CharField | M/F/O. |
| `date_of_birth` | DateField | DOB. |
| `mobile` | CharField | Contact number. |
| `address` | TextField | Home address. |
| `salary` | DecimalField | Monthly salary. |
| `contract_type` | CharField | Full-Time, Part-Time, etc. |
| `photo` | ImageField | Profile picture. |
| `hire_date` | DateField | Date of joining. |

---

## 5. Student App (`student`)
**Purpose:** Manages Student Admission and Records.

### Model: `Student`
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary Key |
| `user` | OneToOneField (User) | Link to Django User (Authentication). |
| `institution` | ForeignKey (Institution) | Enrolled institution. |
| `course` | ForeignKey (Course) | Primary enrolled course/major. |
| `student_id` | CharField | Unique Roll Number. |
| `academic_year` | CharField | e.g., "2023-2024". |
| `gender` | CharField | M/F/O. |
| `date_of_birth` | DateField | DOB. |
| `blood_group` | CharField | Medical info. |
| `address` | TextField | Home address. |
| `parent_name` | CharField | Guardian name. |
| `parent_phone` | CharField | Guardian contact. |
| `gpa` | FloatField | Current GPA. |
| `status` | CharField | Active/Inactive. |
| `enrollment_date` | DateField | Date of admission. |

---



## Database Relationships Summary
1. **Institution -> All**: Is the root parent. All other models (Teacher, Student, Course) link back to an Institution.
2. **User -> Profile**: Django built-in `User` maps to `UserProfile` for role management, and to `Teacher`/`Student` models for specific data.
3. **Course -> Teacher**: Many-to-Many relationship (A course can have multiple teachers; a teacher can teach multiple courses).
4. **Student -> Course**: Foreign Key (One student has one primary course/major) - *Note: This might be expanded to Many-to-Many in future if elective support is needed.*
5. **Grade -> Student+Course**: Link specific students to their performance in specific courses.
