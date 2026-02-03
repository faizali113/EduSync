from django.db import models
from django.contrib.auth.models import User
from institution.models import Institution

class Student(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    course = models.ForeignKey('academics.Course', on_delete=models.SET_NULL, null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    academic_year = models.CharField(max_length=20, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    gpa = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"
