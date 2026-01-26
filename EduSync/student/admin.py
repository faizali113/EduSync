from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'institution', 'status', 'gpa')
    list_filter = ('status', 'institution')
    search_fields = ('student_id', 'user__username')
