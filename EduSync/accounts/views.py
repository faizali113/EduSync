from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from .models import UserProfile
from institution.models import Institution

@require_http_methods(["GET", "POST"])
def landing_view(request):
    return render(request, 'landing.html')

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if username exists
        if not User.objects.filter(username=username).exists():
            return render(request, 'login.html', {'error': '❌ Username does not exist. Please sign up first.'})
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Role-based redirect with success message
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'institution_admin':
                    return render(request, 'login.html', {'success': '✅ Login successfully! Redirecting to dashboard...', 'redirect': 'dashboard'})
                elif profile.role == 'teacher':
                    return render(request, 'login.html', {'success': '✅ Login successfully! Redirecting to dashboard...', 'redirect': 'teacher_dashboard'})
                elif profile.role == 'student':
                    return render(request, 'login.html', {'success': '✅ Login successfully! Redirecting to dashboard...', 'redirect': 'student_dashboard'})
            except UserProfile.DoesNotExist:
                return redirect('landing')
        else:
            return render(request, 'login.html', {'error': '❌ Invalid password. Please try again.'})
    
    return render(request, 'login.html')

@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.method == 'POST':
        institution_name = request.POST.get('institution')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if institution name already exists
        if Institution.objects.filter(name=institution_name).exists():
            return render(request, 'signup.html', {'error': 'Institution already exists'})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': '❌ Username already exists. Please choose a different username.'})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': '❌ Email already registered. Please use a different email.'})
        
        try:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Create UserProfile as institution admin
            UserProfile.objects.create(user=user, role='institution_admin', institution=institution_name)
            
            # Create Institution
            Institution.objects.create(name=institution_name, admin=user, email=email)
            
            login(request, user)
            
            # Render with success message and redirect
            return render(request, 'signup.html', {'success': '✅ Sign up successfully! Redirecting to dashboard...', 'redirect': 'login'})
        except Exception as e:
            return render(request, 'signup.html', {'error': f'❌ Error creating account: {str(e)}'})
    
    return render(request, 'signup.html')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('landing')


