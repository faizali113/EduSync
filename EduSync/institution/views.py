from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Institution, News


# 🔹 INSTITUTION DASHBOARD (WELCOME PAGE)
@login_required(login_url='login')
def dashboard_view(request):
    try:
        institution = Institution.objects.get(admin=request.user)
    except Institution.DoesNotExist:
        institution = None

    news_list = News.objects.order_by("-created_at")

    context = {
        'institution': institution,
        'user': request.user,
        'news_list': news_list,          # ✅ NEWS PASSED HERE
        'show_dashboard_nav': True,
    }

    return render(request, 'institution/dashboard.html', context)


# 🔹 INSTITUTION ADMIN LOGIN
def institution_admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            context = {
                'error': "❌ Username or password is wrong",
                'redirect': 'dashboard'
            }
            return render(request, 'institution/admin_login.html', context)

        if user.userprofile.role != 'institution_admin':
            context = {
                'error': "❌ You are not an institution admin",
                'redirect': 'dashboard'
            }
            return render(request, 'institution/admin_login.html', context)

        login(request, user)
        context = {
            'success': "✅ Login successful, moving to admin dashboard",
            'redirect': 'institution_admin_dashboard',
            'force_public_nav': True
        }
        return render(request, 'institution/admin_login.html', context)

    return render(
        request,
        'institution/admin_login.html'
    )


# 🔹 INSTITUTION ADMIN DASHBOARD (ADD + SHOW NEWS)
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
