from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('timetable/', views.teacher_timetable, name='teacher_timetable'),
    path('attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('students/', views.teacher_students, name='teacher_students'),
]