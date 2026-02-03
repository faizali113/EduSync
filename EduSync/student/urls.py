from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('grades/', views.student_grades, name='student_grades'),
    path('list/', views.student_list, name='student_list'),
    path('add/', views.student_create, name='student_create'),
    path('edit/<int:student_id>/', views.student_edit, name='student_edit'),
    path('delete/<int:student_id>/', views.student_delete, name='student_delete'),
]
