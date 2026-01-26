from django.contrib import admin
from .models import Course, Grade

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher', 'credits')
    list_filter = ('institution', 'teacher')
    search_fields = ('code', 'name')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'marks')
    list_filter = ('grade', 'course')
    search_fields = ('student__user__username', 'course__code')
