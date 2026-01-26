from django.db import models
from academics.models import Course

class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday')
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)
    
    class Meta:
        unique_together = ('course', 'day', 'start_time')
    
    def __str__(self):
        return f"{self.course.code} - {self.day} {self.start_time}-{self.end_time}"

class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('course', 'student', 'date')
    
    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.student} - {self.course} ({self.date}): {status}"
