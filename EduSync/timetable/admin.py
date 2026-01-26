from django.contrib import admin
from .models import TimeSlot, Attendance

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('course', 'day', 'start_time', 'end_time', 'room')
    list_filter = ('day', 'course')
    search_fields = ('course__code', 'room')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'present')
    list_filter = ('date', 'present', 'course')
    search_fields = ('student__user__username', 'course__code')
