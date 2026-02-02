from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from .models import UserProfile, LoginTable
from institution.models import Institution

@require_http_methods(["GET", "POST"])
def landing_view(request):
    return render(request, 'landing.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        from .models import SignupTable
        institution_name = request.POST.get('institution_name')
        password = request.POST.get('password')
        
        # Check if institution exists in SignupTable first
        try:
            signup = SignupTable.objects.get(institution_name=institution_name)
        except SignupTable.DoesNotExist:
            return render(request, 'login.html', {'error': '❌ Institution does not exist. Please sign up first.'})
        
        # Check if LoginTable entry exists, if not create it
        try:
            login_entry = LoginTable.objects.get(institution_name=institution_name)
        except LoginTable.DoesNotExist:
            # Create LoginTable entry if it doesn't exist
            login_entry = LoginTable.objects.create(
                signup=signup,
                institution_name=institution_name,
                password=password
            )
        
        # Verify password
        if login_entry.password != password:
            return render(request, 'login.html', {'error': '❌ Invalid password. Please try again.'})
        
        # Get the associated User
        user = User.objects.filter(userprofile__institution=signup.institution_name, userprofile__role='institution_admin').first()
        if user is None:
            return render(request, 'login.html', {'error': '❌ User account not found.'})

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
    
    return render(request, 'login.html')

@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.method == 'POST':
        from .models import SignupTable
        institution_name = request.POST.get('institution')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if institution name already exists
        if Institution.objects.filter(name=institution_name).exists():
            return render(request, 'signup.html', {'error': 'Institution already exists'})
        
        if SignupTable.objects.filter(institution_name=institution_name).exists():
            return render(request, 'signup.html', {'error': 'Institution name already registered'})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': '❌ Username already exists. Please choose a different username.'})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': '❌ Email already registered. Please use a different email.'})
        
        try:
            # Create SignupTable entry (institution details)
            signup = SignupTable.objects.create(
                institution_name=institution_name,
                email=email
            )
            
            # Create LoginTable entry (login credentials)
            LoginTable.objects.create(
                signup=signup,
                institution_name=institution_name,
                password=password
            )
            
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Create UserProfile as institution admin
            UserProfile.objects.create(user=user, role='institution_admin', institution=institution_name)
            
            # Create Institution
            Institution.objects.create(name=institution_name, admin=user, email=email)
            
            login(request, user)
            
            # Render with success message and redirect
            return render(request, 'signup.html', {'success': '✅ Sign up successfully! Redirecting to login...', 'redirect': 'login'})
        except Exception as e:
            return render(request, 'signup.html', {'error': f'❌ Error creating account: {str(e)}'})
    
    return render(request, 'signup.html')

def logout_view(request):
    next_url = request.GET.get('next')

    logout(request)

    if next_url:
        return redirect(next_url)   # Redirect where navbar asked

    return redirect('landing') 

