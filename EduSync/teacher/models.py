from django.db import models
from django.contrib.auth.models import User
from institution.models import Institution

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    hire_date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
