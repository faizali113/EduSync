from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Teacher
from academics.models import Course
from timetable.models import TimeSlot, Attendance
from student.models import Student
from institution.models import Institution
from accounts.models import UserProfile
from .forms import TeacherCreateForm, TeacherEditForm


def _get_institution_admin(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return None, 'User profile not found.'

    if profile.role != 'institution_admin':
        return None, 'Only institution admins can access this page.'

    try:
        institution = Institution.objects.get(admin=request.user)
    except Institution.DoesNotExist:
        return None, 'No institution is linked to this account.'

    return institution, None


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


@login_required(login_url='login')
def teacher_list(request):
    institution, error = _get_institution_admin(request)
    if error:
        return render(request, 'teacher/teacher_list.html', {'error': error})

    teachers = Teacher.objects.filter(institution=institution).select_related('user')
    return render(request, 'teacher/teacher_list.html', {'teachers': teachers})


@login_required(login_url='login')
def teacher_create(request):
    institution, error = _get_institution_admin(request)
    if error:
        return render(request, 'teacher/teacher_form.html', {'error': error})

    if request.method == 'POST':
        form = TeacherCreateForm(request.POST, institution=institution)
        if form.is_valid():
            teacher = form.save(institution=institution)
            UserProfile.objects.create(
                user=teacher.user,
                role='teacher',
                institution=institution.name
            )
            return redirect('teacher_list')
    else:
        form = TeacherCreateForm(institution=institution)

    return render(request, 'teacher/teacher_form.html', {'form': form, 'mode': 'create'})


@login_required(login_url='login')
def teacher_edit(request, teacher_id):
    institution, error = _get_institution_admin(request)
    if error:
        return render(request, 'teacher/teacher_form.html', {'error': error})

    teacher = get_object_or_404(Teacher, id=teacher_id, institution=institution)

    if request.method == 'POST':
        form = TeacherEditForm(request.POST, teacher=teacher, institution=institution)
        if form.is_valid():
            teacher.user.username = form.cleaned_data['username']
            teacher.user.first_name = form.cleaned_data['first_name']
            teacher.user.last_name = form.cleaned_data['last_name']
            teacher.user.email = form.cleaned_data['email']
            teacher.user.save()

            teacher.employee_id = form.cleaned_data['employee_id']
            teacher.department = form.cleaned_data['department']
            teacher.qualification = form.cleaned_data['qualification']
            teacher.phone = form.cleaned_data.get('phone', '')
            teacher.save()

            selected_courses = set(form.cleaned_data.get('courses', []))
            current_courses = set(Course.objects.filter(teachers=teacher))

            for course in current_courses - selected_courses:
                course.teachers.remove(teacher)
            for course in selected_courses - current_courses:
                course.teachers.add(teacher)

            return redirect('teacher_list')
    else:
        form = TeacherEditForm(teacher=teacher, institution=institution)

    return render(request, 'teacher/teacher_form.html', {
        'form': form,
        'mode': 'edit',
        'teacher': teacher
    })


@login_required(login_url='login')
def teacher_delete(request, teacher_id):
    institution, error = _get_institution_admin(request)
    if error:
        return render(request, 'teacher/teacher_list.html', {'error': error})

    teacher = get_object_or_404(Teacher, id=teacher_id, institution=institution)
    user = teacher.user
    teacher.delete()
    user.delete()
    return redirect('teacher_list')
