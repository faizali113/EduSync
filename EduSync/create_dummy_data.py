import os
import django
import random
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EduSync.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import SignupTable, LoginTable, UserProfile
from institution.models import Institution
from teacher.models import Teacher
from academics.models import Course, Grade
from student.models import Student

def create_institution():
    print("Creating/Getting Institution...")
    inst_name = "Tech University"
    
    # Check if exists
    if Institution.objects.filter(name=inst_name).exists():
        print(f"Institution '{inst_name}' already exists.")
        return Institution.objects.get(name=inst_name)

    # Create Admin User
    admin_username = "admin_tech"
    if not User.objects.filter(username=admin_username).exists():
        admin_user = User.objects.create_user(username=admin_username, email="admin@tech.edu", password="password123")
        admin_user.first_name = "Admin"
        admin_user.last_name = "User"
        admin_user.save()
    else:
        admin_user = User.objects.get(username=admin_username)

    # Create SignupTable entry
    signup, created = SignupTable.objects.get_or_create(
        institution_name=inst_name,
        defaults={
            'email': "info@tech.edu",
            'phone': "1234567890",
            'address': "123 Tech Lane, Silicon Valley"
        }
    )

    # Create Institution
    institution, created = Institution.objects.get_or_create(
        name=inst_name,
        defaults={
            'admin': admin_user,
            'email': "contact@tech.edu",
            'phone': "0987654321",
            'address': "123 Tech Lane, Silicon Valley",
            'established_year': 1990
        }
    )

    # User Profile for Admin
    UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'role': 'institution_admin',
            'institution': inst_name,
            'phone': "0987654321"
        }
    )

    return institution

def create_teachers(institution):
    print("Creating Teachers...")
    departments = ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology']
    teachers = []
    
    for i in range(1, 6):
        username = f"teacher_{i}"
        user = None
        if User.objects.filter(username=username).exists():
            print(f"User {username} already exists.")
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(username=username, email=f"{username}@tech.edu", password="password123")
            user.first_name = f"Teacher"
            user.last_name = f"{i}"
            user.save()

        # Ensure UserProfile exists
        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'teacher',
                'institution': institution.name,
                'phone': f"555000{i}"
            }
        )

        # Ensure Teacher entry exists
        if Teacher.objects.filter(user=user).exists():
             teacher = Teacher.objects.get(user=user)
        else:
             teacher = Teacher.objects.create(
                user=user,
                institution=institution,
                employee_id=f"EMP{i:03d}",
                department=random.choice(departments),
                qualification="PhD",
                gender=random.choice(['M', 'F']),
                phone=f"555000{i}",
                address=f"Address {i}",
                salary=50000 + (i * 1000)
            )
        
        teachers.append(teacher)
        print(f"Processed Teacher: {username}")
    
    return teachers

def create_courses(institution, teachers):
    print("Creating Courses...")
    course_data = [
        ("CS101", "Intro to Programming", "Computer Science"),
        ("MATH101", "Calculus I", "Mathematics"),
        ("PHY101", "Physics I", "Physics"),
        ("CHEM101", "Organic Chemistry", "Chemistry"),
        ("BIO101", "Biology Basics", "Biology")
    ]
    
    courses = []
    for code, name, dept in course_data:
        course, created = Course.objects.get_or_create(
            institution=institution,
            code=code,
            defaults={
                'name': name,
                'description': f"Description for {name}",
                'credits': 3,
                'department': dept,
                'tuition_fee': 1000.00
            }
        )
        if created:
            # Assign random teachers
            course.teachers.set(random.sample(teachers, k=min(len(teachers), 2)))
            print(f"Created Course: {name}")
        else:
            print(f"Course {name} already exists.")
        courses.append(course)

    return courses

def create_students(institution, courses):
    print("Creating Students...")
    students = []
    
    for i in range(1, 21):
        username = f"student_{i}"
        user = None
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(username=username, email=f"{username}@tech.edu", password="password123")
            user.first_name = f"Student"
            user.last_name = f"{i}"
            user.save()

        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'student',
                'institution': institution.name,
                'phone': f"999000{i}"
            }
        )
        
        assigned_course = random.choice(courses)

        if Student.objects.filter(user=user).exists():
            student = Student.objects.get(user=user)
        else:
            student = Student.objects.create(
                user=user,
                institution=institution,
                student_id=f"STU{i:03d}",
                course=assigned_course,
                academic_year="2025-2026",
                gender=random.choice(['M', 'F']),
                date_of_birth=date(2000, 1, 1) + timedelta(days=random.randint(0, 365*5)),
                parent_name=f"Parent {i}",
                parent_phone=f"888000{i}",
                blood_group=random.choice(['A+', 'B+', 'O+', 'AB+']),
                status='active'
            )
        students.append(student)
        print(f"Processed Student: {username}")
        
    return students

def create_grades(students, courses):
    print("Creating Grades...")
    for student in students:
        # Assign grades for random courses (including their main course)
        # Assuming students can take multiple courses, but here Grade model links Student and Course
        
        # Add grades for their assigned course
        if student.course:
            if not Grade.objects.filter(student=student, course=student.course).exists():
                Grade.objects.create(
                    student=student,
                    course=student.course,
                    grade=random.choice(['A', 'B', 'C', 'D', 'F']),
                    marks=random.uniform(40, 100)
                )
                print(f"Assigned grade for {student} in {student.course}")

        # Maybe one more random course
        random_course = random.choice(courses)
        if random_course != student.course:
             if not Grade.objects.filter(student=student, course=random_course).exists():
                Grade.objects.create(
                    student=student,
                    course=random_course,
                    grade=random.choice(['A', 'B', 'C', 'D', 'F']),
                    marks=random.uniform(40, 100)
                )
                print(f"Assigned grade for {student} in {random_course}")


if __name__ == "__main__":
    inst = create_institution()
    teachers = create_teachers(inst)
    courses = create_courses(inst, teachers)
    students = create_students(inst, courses)
    create_grades(students, courses)
    print("Dummy data generation complete!")
