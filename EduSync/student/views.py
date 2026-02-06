from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student
from academics.models import Grade
from institution.models import Institution
from accounts.models import UserProfile
from django.db import transaction, IntegrityError
from .forms import StudentCreateForm, StudentEditForm


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
        messages.error(request, 'Student not found.')
        return redirect('dashboard')

@login_required(login_url='login')
def student_grades(request):
    try:
        student = Student.objects.get(user=request.user)
        grades = Grade.objects.filter(student=student).select_related('course')
        context = {'grades': grades, 'student': student}
        return render(request, 'student/grades.html', context)
    except Student.DoesNotExist:
        return render(request, 'student/grades.html', {'error': 'Student profile not found'})


@login_required(login_url='login')
def student_list(request):
    institution, error = _get_institution_admin(request)
    if error:
        return render(request, 'student/student_list.html', {'error': error})

    students = Student.objects.filter(institution=institution).select_related('user', 'course')
    return render(request, 'student/student_list.html', {'students': students})


@login_required(login_url='login')
def student_create(request):
    institution, error = _get_institution_admin(request)
    if error:
        return render(request, 'student/student_form.html', {'error': error})

    if request.method == 'POST':
        form = StudentCreateForm(request.POST, institution=institution)
        if form.is_valid():
            try:
                with transaction.atomic():

                    full_name = form.cleaned_data['name'].strip()
                    parts = full_name.split(None, 1)
                    first_name = parts[0] if parts else full_name
                    last_name = parts[1] if len(parts) > 1 else ""
                    student_id = form.cleaned_data['student_id']
                    username = _unique_username(f"student_{student_id}")
                    password = student_id

                    user = User.objects.create_user(username=username, password=password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    student = Student.objects.create(
                        user=user,
                        institution=institution,
                        student_id=student_id,
                        academic_year=form.cleaned_data.get('academic_year', ''),
                        gender=form.cleaned_data['gender'],
                        date_of_birth=form.cleaned_data.get('date_of_birth'),
                        address=form.cleaned_data.get('address', ''),
                        parent_name=form.cleaned_data.get('parent_name', ''),
                        parent_phone=form.cleaned_data.get('parent_phone', ''),
                        blood_group=form.cleaned_data.get('blood_group', ''),
                        course=form.cleaned_data.get('course'),
                    )

                    UserProfile.objects.create(
                        user=student.user,
                        role='student',
                        institution=institution.name
                    )
                messages.success(request, 'Student added successfully.')
                return redirect('student_list')
            except IntegrityError as e:
                messages.error(request, f'Database error: One of the unique fields (like Roll No) might already exist. ({e})')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}')
    else:
        form = StudentCreateForm(institution=institution)

    return render(request, 'student/student_form.html', {'form': form, 'mode': 'create'})


@login_required(login_url='login')
def student_edit(request, student_id):
    institution, error = _get_institution_admin(request)
    if error:
        return render(request, 'student/student_form.html', {'error': error})

    student = get_object_or_404(Student, id=student_id, institution=institution)

    if request.method == 'POST':
        form = StudentEditForm(request.POST, student=student, institution=institution)
        if form.is_valid():
            full_name = form.cleaned_data['name'].strip()
            parts = full_name.split(None, 1)
            student.user.first_name = parts[0] if parts else full_name
            student.user.last_name = parts[1] if len(parts) > 1 else ''
            student.user.save()

            student.student_id = form.cleaned_data['student_id']
            student.academic_year = form.cleaned_data.get('academic_year', '')
            student.gender = form.cleaned_data['gender']
            student.date_of_birth = form.cleaned_data.get('date_of_birth')
            student.address = form.cleaned_data.get('address', '')
            student.parent_name = form.cleaned_data.get('parent_name', '')
            student.parent_phone = form.cleaned_data.get('parent_phone', '')
            student.blood_group = form.cleaned_data.get('blood_group', '')
            student.course = form.cleaned_data.get('course')
            student.save()

            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentEditForm(student=student, institution=institution)

    return render(request, 'student/student_form.html', {
        'form': form,
        'mode': 'edit',
        'student': student
    })


@login_required(login_url='login')
def student_delete(request, student_id):
    institution, error = _get_institution_admin(request)
    if error:
        return render(request, 'student/student_list.html', {'error': error})

    student = get_object_or_404(Student, id=student_id, institution=institution)
    user = student.user
    student.delete()
    user.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('student_list')
