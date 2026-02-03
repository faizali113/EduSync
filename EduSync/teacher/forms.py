from django import forms
from academics.models import Course


class TeacherCreateForm(forms.Form):
    name = forms.CharField(max_length=150, label="Teacher Name")
    employee_id = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    qualification = forms.CharField(max_length=200)
    photo = forms.ImageField(required=False)
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, institution=None, **kwargs):
        super().__init__(*args, **kwargs)
        if institution is not None:
            self.fields["courses"].queryset = Course.objects.filter(institution=institution)


class TeacherEditForm(forms.Form):
    name = forms.CharField(max_length=150, label="Teacher Name")
    employee_id = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    qualification = forms.CharField(max_length=200)
    photo = forms.ImageField(required=False)
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, teacher=None, institution=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.teacher = teacher
        if institution is not None:
            self.fields["courses"].queryset = Course.objects.filter(institution=institution)
        if teacher is not None:
            self.fields["name"].initial = teacher.user.get_full_name() or teacher.user.username
            self.fields["employee_id"].initial = teacher.employee_id
            self.fields["department"].initial = teacher.department
            self.fields["qualification"].initial = teacher.qualification
            self.fields["courses"].initial = Course.objects.filter(teachers=teacher)

    def clean_employee_id(self):
        employee_id = self.cleaned_data["employee_id"]
        return employee_id
