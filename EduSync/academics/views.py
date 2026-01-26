from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course, Grade

@login_required(login_url='login')
def course_list(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'academics/course_list.html', context)

@login_required(login_url='login')
def course_detail(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        grades = Grade.objects.filter(course=course)
        context = {'course': course, 'grades': grades}
        return render(request, 'academics/course_detail.html', context)
    except Course.DoesNotExist:
        return render(request, 'academics/course_detail.html', {'error': 'Course not found'})
