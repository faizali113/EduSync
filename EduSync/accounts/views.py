from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from .models import UserProfile, SignupTable, LoginTable
from institution.models import Institution

@require_http_methods(["GET", "POST"])
def landing_view(request):
    return render(request, 'landing.html')

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if username exists in LoginTable
        try:
            login_record = LoginTable.objects.get(username=username)
        except LoginTable.DoesNotExist:
            return render(request, 'login.html', {'error': 'Username is not exists'})
        
        # Check if password matches
        if login_record.password == password:
            # Get signup details
            signup = login_record.signup
            
            # Check if institution exists
            try:
                institution = Institution.objects.get(name=signup.institution_name)
                # Login successful - redirect to dashboard
                request.session['institution_id'] = institution.id
                request.session['username'] = username
                return render(request, 'login.html', {'success': 'Login successfully', 'redirect': 'dashboard'})
            except Institution.DoesNotExist:
                return render(request, 'login.html', {'error': 'Institution not found'})
        else:
            return render(request, 'login.html', {'error': 'Password is not correct'})
    
    return render(request, 'login.html')

@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.method == 'POST':
        institution_name = request.POST.get('institution')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # ONLY check if institution name already exists in SignupTable
        if SignupTable.objects.filter(institution_name=institution_name).exists():
            return render(request, 'signup.html', {'error': 'Institution is already exists'})
        
        try:
            # Create SignupTable record
            signup = SignupTable.objects.create(
                institution_name=institution_name,
                email=email
            )
            
            # Create LoginTable record
            LoginTable.objects.create(
                signup=signup,
                username=username,
                password=password
            )
            
            # Create Institution record
            Institution.objects.create(
                name=institution_name,
                admin=None,
                email=email
            )
            
            return render(request, 'signup.html', {'success': 'Sign up successfully', 'redirect': 'login'})
        except Exception as e:
            return render(request, 'signup.html', {'error': f'Error: {str(e)}'})
    
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    if 'institution_id' in request.session:
        del request.session['institution_id']
    if 'username' in request.session:
        del request.session['username']
    return redirect('landing')