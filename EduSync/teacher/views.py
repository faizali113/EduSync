from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Teacher
from academics.models import Course
from timetable.models import TimeSlot, Attendance
from student.models import Student
from institution.models import Institution
from accounts.models import UserProfile
from .forms import TeacherCreateForm, TeacherEditForm


def _unique_username(base):
    from django.contrib.auth.models import User
    username = base
    suffix = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{suffix}"
        suffix += 1
    return username


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
        form = TeacherCreateForm(request.POST, request.FILES, institution=institution)
        if form.is_valid():
            from django.contrib.auth.models import User
            full_name = form.cleaned_data['name'].strip()
            parts = full_name.split(None, 1)
            first_name = parts[0] if parts else full_name
            last_name = parts[1] if len(parts) > 1 else ""
            employee_id = form.cleaned_data['employee_id']
            username = _unique_username(f"teacher_{employee_id}")
            password = employee_id

            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            teacher = Teacher.objects.create(
                user=user,
                institution=institution,
                employee_id=employee_id,
                department=form.cleaned_data['department'],
                qualification=form.cleaned_data['qualification'],
                photo=form.cleaned_data.get('photo'),
            )

            courses = form.cleaned_data.get('courses')
            if courses:
                for course in courses:
                    course.teachers.add(teacher)

            UserProfile.objects.create(
                user=teacher.user,
                role='teacher',
                institution=institution.name
            )
            messages.success(request, 'Teacher added successfully.')
            messages.success(request, 'Teacher updated successfully.')
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
        form = TeacherEditForm(request.POST, request.FILES, teacher=teacher, institution=institution)
        if form.is_valid():
            full_name = form.cleaned_data['name'].strip()
            parts = full_name.split(None, 1)
            teacher.user.first_name = parts[0] if parts else full_name
            teacher.user.last_name = parts[1] if len(parts) > 1 else ''
            teacher.user.save()

            teacher.employee_id = form.cleaned_data['employee_id']
            teacher.department = form.cleaned_data['department']
            teacher.qualification = form.cleaned_data['qualification']
            if form.cleaned_data.get('photo'):
                teacher.photo = form.cleaned_data.get('photo')
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
    messages.success(request, 'Teacher deleted successfully.')
    return redirect('teacher_list')
