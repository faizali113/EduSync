from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/login/', views.institution_admin_login, name='institution_admin_login'),
    path('admin/dashboard/', views.institution_admin_dashboard, name='institution_admin_dashboard'),
    path('news/delete/<int:news_id>/', views.delete_news, name='delete_news'),
]
