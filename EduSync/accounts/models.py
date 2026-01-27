from django.db import models
from django.contrib.auth.models import User

class SignupTable(models.Model):
    """Stores institution details during signup"""
    institution_name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.institution_name

class LoginTable(models.Model):
    """Stores login credentials"""
    signup = models.OneToOneField(SignupTable, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=200, unique=True, null=True, blank=True)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.institution_name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('institution_admin', 'Institution Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='institution_admin')
    phone = models.CharField(max_length=15, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
