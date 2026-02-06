from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from .models import Institution, News
from academics.models import Course
from teacher.models import Teacher
from student.models import Student


# 🔹 INSTITUTION DASHBOARD (WELCOME PAGE)
@never_cache
@login_required(login_url='login')
def dashboard_view(request):
    # 🛡️ ROLE CHECK: Redirect non-admins to their respective dashboards
    if hasattr(request.user, 'userprofile'):
        role = request.user.userprofile.role
        if role == 'student':
            return redirect('student_dashboard')
        elif role == 'teacher':
            return redirect('teacher_dashboard')

    try:
        institution = Institution.objects.get(admin=request.user)
    except Institution.DoesNotExist:
        institution = None

    news_list = News.objects.order_by("-created_at")
    courses = Course.objects.filter(institution=institution) if institution else Course.objects.none()
    teachers = Teacher.objects.filter(institution=institution) if institution else Teacher.objects.none()

    context = {
        'institution': institution,
        'user': request.user,
        'news_list': news_list,
        'courses': courses,
        'teachers': teachers,
        'show_dashboard_nav': True,
    }

    return render(request, 'institution/dashboard.html', context)


@login_required(login_url='login')
def teacher_portal_login(request):
    return _handle_portal_login(request, role='teacher')


@login_required(login_url='login')
def student_portal_login(request):
    return _handle_portal_login(request, role='student')



def _handle_portal_login(request, role):
    if request.method == "GET":
        context = {
            'role': role,
            'title': 'Teacher Login' if role == 'teacher' else 'Student Login',
            'name_label': 'Teacher Name' if role == 'teacher' else 'Student Name',
            'code_label': 'Employee ID' if role == 'teacher' else 'Roll No.',
            'name_placeholder': 'Enter teacher name' if role == 'teacher' else 'Enter student name',
            'code_placeholder': 'Enter employee ID' if role == 'teacher' else 'Enter roll number',
        }
        return render(request, 'institution/portal_login.html', context)

    name = " ".join((request.POST.get('name') or "").split())
    code = (request.POST.get('code') or "").strip()

    try:
        institution = Institution.objects.get(admin=request.user)
    except Institution.DoesNotExist:
        messages.error(request, 'Institution not found for this account.')
        return redirect('dashboard')

    def normalize(value):
        return " ".join((value or "").split()).lower()

    if role == "teacher":
        teacher = Teacher.objects.filter(employee_id=code, institution=institution).select_related('user').first()
        if not teacher:
            messages.error(request, 'Teacher not found.')
            return redirect('teacher_portal_login')

        full_name = teacher.user.get_full_name()
        user_name = teacher.user.username
        expected_names = {normalize(full_name), normalize(user_name)}
        if normalize(name) not in expected_names:
            messages.error(request, 'Teacher not found.')
            return redirect('teacher_portal_login')

        user = authenticate(request, username=teacher.user.username, password=code)
        if user is None:
            messages.error(request, 'Invalid teacher credentials.')
            return redirect('teacher_portal_login')

        logout(request)
        login(request, user)
        return redirect('teacher_dashboard')

    if role == "student":
        student = Student.objects.filter(student_id=code, institution=institution).select_related('user').first()
        if not student:
            messages.error(request, 'Student not found.')
            return redirect('student_portal_login')

        full_name = student.user.get_full_name()
        user_name = student.user.username
        print(full_name, user_name,code)
        expected_names = {normalize(full_name), normalize(user_name)}
        if normalize(name) not in expected_names:
            messages.error(request, 'Student not found.')
            return redirect('student_portal_login')

        user = authenticate(request, username=student.user.username, password=code)
        if user is None:
            messages.error(request, 'Invalid student credentials.')
            return redirect('student_portal_login')

        logout(request)
        login(request, user)
        return redirect('student_dashboard')

    messages.error(request, 'Invalid login request.')
    return redirect('dashboard')


def institution_admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'institution/admin_login.html', {'error': "❌ Username or password is wrong"})

        if not hasattr(user, 'userprofile') or user.userprofile.role != 'institution_admin':
            return render(request, 'institution/admin_login.html', {'error': "❌ You are not an institution admin"})

        login(request, user)
        messages.success(request, "✅ Login successful, welcome to the admin dashboard!")
        return redirect('institution_admin_dashboard')

    return render(
        request,
        'institution/admin_login.html'
    )


# 🔹 INSTITUTION ADMIN DASHBOARD (ADD + SHOW NEWS)
@never_cache
@login_required(login_url='institution_admin_login')
def institution_admin_dashboard(request):
    edit_news = None

    # EDIT MODE
    edit_id = request.GET.get("edit")
    if edit_id:
        edit_news = News.objects.filter(id=edit_id).first()

    # CREATE / UPDATE
    if request.method == "POST":
        news_text = request.POST.get("news")
        news_id = request.POST.get("news_id")

        if news_text:
            if news_id:
                # UPDATE
                news = News.objects.get(id=news_id)
                news.content = news_text
                news.save()
            else:
                # CREATE
                News.objects.create(content=news_text)

        return redirect("institution_admin_dashboard")

    news_list = News.objects.order_by("-created_at")

    return render(
        request,
        "institution/admin_dashboard.html",
        {
            "news_list": news_list,
            "edit_news": edit_news,
            "show_dashboard_nav": True,
            "admin_dashboard_mode": True
            
        }
    )

@login_required
def delete_news(request, news_id):
    News.objects.filter(id=news_id).delete()
    return redirect('institution_admin_dashboard')
