from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Institution

@login_required(login_url='login')
def dashboard_view(request):
    try:
        institution = Institution.objects.get(admin=request.user)
    except Institution.DoesNotExist:
        institution = None
    
    context = {
        'institution': institution,
        'user': request.user,
    }
    return render(request, 'institution/dashboard.html', context)