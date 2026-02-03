from django import forms
from academics.models import Course


class StudentCreateForm(forms.Form):
    name = forms.CharField(max_length=150, label="Student Name")
    student_id = forms.CharField(max_length=20, label="Roll No.")
    academic_year = forms.CharField(max_length=20, required=False)
    course = forms.ModelChoiceField(queryset=Course.objects.none(), required=False)

    def __init__(self, *args, institution=None, **kwargs):
        super().__init__(*args, **kwargs)
        if institution is not None:
            self.fields["course"].queryset = Course.objects.filter(institution=institution)


class StudentEditForm(forms.Form):
    name = forms.CharField(max_length=150, label="Student Name")
    student_id = forms.CharField(max_length=20, label="Roll No.")
    academic_year = forms.CharField(max_length=20, required=False)
    course = forms.ModelChoiceField(queryset=Course.objects.none(), required=False)

    def __init__(self, *args, student=None, institution=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.student = student
        if institution is not None:
            self.fields["course"].queryset = Course.objects.filter(institution=institution)
        if student is not None:
            self.fields["name"].initial = student.user.get_full_name() or student.user.username
            self.fields["student_id"].initial = student.student_id
            self.fields["academic_year"].initial = student.academic_year
            self.fields["course"].initial = student.course
