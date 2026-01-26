from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Teacher
from academics.models import Course
from timetable.models import TimeSlot, Attendance
from student.models import Student

@login_required(login_url='login')
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        courses = Course.objects.filter(teacher=teacher)
        context = {
            'teacher': teacher,
            'courses': courses,
        }
        return render(request, 'teacher/dashboard.html', context)
    except Teacher.DoesNotExist:
        return render(request, 'teacher/dashboard.html', {'error': 'Teacher profile not found'})

@login_required(login_url='login')
def teacher_timetable(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        courses = Course.objects.filter(teacher=teacher)
        timetable = TimeSlot.objects.filter(course__in=courses)
        context = {'timetable': timetable, 'teacher': teacher}
        return render(request, 'teacher/timetable.html', context)
    except Teacher.DoesNotExist:
        return render(request, 'teacher/timetable.html', {'error': 'Teacher profile not found'})

@login_required(login_url='login')
def teacher_attendance(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        courses = Course.objects.filter(teacher=teacher)
        attendance = Attendance.objects.filter(course__in=courses)
        context = {'attendance': attendance, 'teacher': teacher, 'courses': courses}
        return render(request, 'teacher/attendance.html', context)
    except Teacher.DoesNotExist:
        return render(request, 'teacher/attendance.html', {'error': 'Teacher profile not found'})

@login_required(login_url='login')
def teacher_students(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        courses = Course.objects.filter(teacher=teacher)
        students = Student.objects.filter(user__id__in=
            Attendance.objects.filter(course__in=courses).values_list('student__user__id', flat=True)).distinct()
        context = {'students': students, 'teacher': teacher}
        return render(request, 'teacher/students.html', context)
    except Teacher.DoesNotExist:
        return render(request, 'teacher/students.html', {'error': 'Teacher profile not found'})
