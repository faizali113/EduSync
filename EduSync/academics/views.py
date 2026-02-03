from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Course, Grade
from .forms import CourseForm
from institution.models import Institution


def _get_user_institution(user):
    try:
        return Institution.objects.get(admin=user)
    except Institution.DoesNotExist:
        return None


@login_required(login_url='login')
def course_list(request):
    institution = _get_user_institution(request.user)
    if institution:
        courses = Course.objects.filter(institution=institution)
    else:
        courses = Course.objects.all()
    context = {'courses': courses, 'institution': institution}
    return render(request, 'academics/course_list.html', context)


@login_required(login_url='login')
def course_detail(request, course_id):
    institution = _get_user_institution(request.user)
    if institution:
        course = get_object_or_404(Course, id=course_id, institution=institution)
    else:
        course = get_object_or_404(Course, id=course_id)
    grades = Grade.objects.filter(course=course)
    context = {'course': course, 'grades': grades}
    return render(request, 'academics/course_detail.html', context)


@login_required(login_url='login')
def course_create(request):
    institution = _get_user_institution(request.user)
    if not institution:
        return render(request, 'academics/course_form.html', {
            'form': None,
            'error': 'No institution is associated with this account.'
        })

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.institution = institution
            course.save()
            form.save_m2m()
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(request, 'academics/course_form.html', {
        'form': form,
        'mode': 'create'
    })


@login_required(login_url='login')
def course_edit(request, course_id):
    institution = _get_user_institution(request.user)
    if institution:
        course = get_object_or_404(Course, id=course_id, institution=institution)
    else:
        course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'academics/course_form.html', {
        'form': form,
        'mode': 'edit',
        'course': course
    })


@login_required(login_url='login')
@require_POST
def course_delete(request, course_id):
    institution = _get_user_institution(request.user)
    if institution:
        course = get_object_or_404(Course, id=course_id, institution=institution)
    else:
        course = get_object_or_404(Course, id=course_id)

    course.delete()
    return redirect('course_list')
