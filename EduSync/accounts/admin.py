from django.contrib import admin
from .models import UserProfile, SignupTable, LoginTable

@admin.register(SignupTable)
class SignupTableAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'email', 'phone', 'created_at')
    search_fields = ('institution_name', 'email')

@admin.register(LoginTable)
class LoginTableAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'signup', 'created_at')
    search_fields = ('institution_name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'institution')
    list_filter = ('role',)
    search_fields = ('user__username',)