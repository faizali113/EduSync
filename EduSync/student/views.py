from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student
from academics.models import Grade

@login_required(login_url='login')
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        grades = Grade.objects.filter(student=student)
        context = {
            'student': student,
            'grades': grades,
        }
        return render(request, 'student/dashboard.html', context)
    except Student.DoesNotExist:
        return render(request, 'student/dashboard.html', {'error': 'Student profile not found'})

@login_required(login_url='login')
def student_grades(request):
    try:
        student = Student.objects.get(user=request.user)
        grades = Grade.objects.filter(student=student).select_related('course')
        context = {'grades': grades, 'student': student}
        return render(request, 'student/grades.html', context)
    except Student.DoesNotExist:
        return render(request, 'student/grades.html', {'error': 'Student profile not found'})
