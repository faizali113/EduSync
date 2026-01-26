from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TimeSlot, Attendance

@login_required(login_url='login')
def timetable_view(request):
    timetable = TimeSlot.objects.all().order_by('day', 'start_time')
    context = {'timetable': timetable}
    return render(request, 'timetable/timetable.html', context)

@login_required(login_url='login')
def attendance_list(request):
    attendance = Attendance.objects.all().order_by('-date')
    context = {'attendance': attendance}
    return render(request, 'timetable/attendance.html', context)
