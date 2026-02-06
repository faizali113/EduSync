from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('students/', views.teacher_students, name='teacher_students'),
    path('list/', views.teacher_list, name='teacher_list'),
    path('add/', views.teacher_create, name='teacher_create'),
    path('edit/<int:teacher_id>/', views.teacher_edit, name='teacher_edit'),
    path('delete/<int:teacher_id>/', views.teacher_delete, name='teacher_delete'),
]
