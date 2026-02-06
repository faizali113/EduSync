from django import forms
from academics.models import Course


from .models import Teacher

class TeacherCreateForm(forms.Form):
    name = forms.CharField(max_length=150, label="Teacher Name")
    employee_id = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    qualification = forms.CharField(max_length=200)
    gender = forms.ChoiceField(choices=Teacher.GENDER_CHOICES)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    salary = forms.DecimalField(max_digits=12, decimal_places=2, initial=0.00)
    contract_type = forms.ChoiceField(choices=Teacher.CONTRACT_CHOICES)
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

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if Teacher.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError("A teacher with this Employee ID already exists.")
        return employee_id


class TeacherEditForm(forms.Form):
    name = forms.CharField(max_length=150, label="Teacher Name")
    employee_id = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    qualification = forms.CharField(max_length=200)
    gender = forms.ChoiceField(choices=Teacher.GENDER_CHOICES)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    salary = forms.DecimalField(max_digits=12, decimal_places=2)
    contract_type = forms.ChoiceField(choices=Teacher.CONTRACT_CHOICES)
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
            self.fields["gender"].initial = teacher.gender
            self.fields["date_of_birth"].initial = teacher.date_of_birth
            self.fields["phone"].initial = teacher.phone
            self.fields["address"].initial = teacher.address
            self.fields["salary"].initial = teacher.salary
            self.fields["contract_type"].initial = teacher.contract_type
            self.fields["courses"].initial = Course.objects.filter(teachers=teacher)

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if Teacher.objects.filter(employee_id=employee_id).exclude(id=self.teacher.id).exists():
            raise forms.ValidationError("A teacher with this Employee ID already exists.")
        return employee_id
