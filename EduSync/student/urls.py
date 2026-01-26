from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('grades/', views.student_grades, name='student_grades'),
]