from django.db import models
from teacher.models import Teacher
from institution.models import Institution


class Course(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE
    )
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    teachers = models.ManyToManyField(
        Teacher, blank=True
    )
    credits = models.IntegerField(default=3)
    duration_months = models.PositiveIntegerField(default=0)
    department = models.CharField(max_length=100, blank=True)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('institution', 'code')

    def __str__(self):
        return f"{self.code} - {self.name}"


class Grade(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ]

    student = models.ForeignKey(
        'student.Student', on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE
    )
    grade = models.CharField(
        max_length=1, choices=GRADE_CHOICES
    )
    marks = models.FloatField()
    date_assigned = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} - {self.course} : {self.grade}"
