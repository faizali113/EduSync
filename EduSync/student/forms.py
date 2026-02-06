from django import forms
from academics.models import Course


from .models import Student

class StudentCreateForm(forms.Form):
    name = forms.CharField(max_length=150, label="Student Name")
    student_id = forms.CharField(max_length=20, label="Roll No.")
    academic_year = forms.CharField(max_length=20, required=False)
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    parent_name = forms.CharField(max_length=150, required=False)
    parent_phone = forms.CharField(max_length=15, required=False)
    blood_group = forms.CharField(max_length=5, required=False)
    course = forms.ModelChoiceField(queryset=Course.objects.none(), required=False)

    def __init__(self, *args, institution=None, **kwargs):
        super().__init__(*args, **kwargs)
        if institution is not None:
            self.fields["course"].queryset = Course.objects.filter(institution=institution)

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("A student with this Roll No. already exists.")
        return student_id


class StudentEditForm(forms.Form):
    name = forms.CharField(max_length=150, label="Student Name")
    student_id = forms.CharField(max_length=20, label="Roll No.")
    academic_year = forms.CharField(max_length=20, required=False)
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    parent_name = forms.CharField(max_length=150, required=False)
    parent_phone = forms.CharField(max_length=15, required=False)
    blood_group = forms.CharField(max_length=5, required=False)
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
            self.fields["gender"].initial = student.gender
            self.fields["date_of_birth"].initial = student.date_of_birth
            self.fields["address"].initial = student.address
            self.fields["parent_name"].initial = student.parent_name
            self.fields["parent_phone"].initial = student.parent_phone
            self.fields["blood_group"].initial = student.blood_group
            self.fields["course"].initial = student.course

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if Student.objects.filter(student_id=student_id).exclude(id=self.student.id).exists():
            raise forms.ValidationError("A student with this Roll No. already exists.")
        return student_id
