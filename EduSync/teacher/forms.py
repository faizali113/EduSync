from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Teacher
from academics.models import Course


class TeacherCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    employee_id = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    qualification = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=15, required=False)
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "employee_id",
            "department",
            "qualification",
            "phone",
            "courses",
        )

    def __init__(self, *args, institution=None, **kwargs):
        super().__init__(*args, **kwargs)
        if institution is not None:
            self.fields["courses"].queryset = Course.objects.filter(institution=institution)

    def save(self, institution=None, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            teacher = Teacher.objects.create(
                user=user,
                institution=institution,
                employee_id=self.cleaned_data["employee_id"],
                department=self.cleaned_data["department"],
                qualification=self.cleaned_data["qualification"],
                phone=self.cleaned_data.get("phone", ""),
            )
            courses = self.cleaned_data.get("courses")
            if courses:
                for course in courses:
                    course.teachers.add(teacher)
            return teacher
        return user


class TeacherEditForm(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    employee_id = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    qualification = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=15, required=False)
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
            self.fields["username"].initial = teacher.user.username
            self.fields["first_name"].initial = teacher.user.first_name
            self.fields["last_name"].initial = teacher.user.last_name
            self.fields["email"].initial = teacher.user.email
            self.fields["employee_id"].initial = teacher.employee_id
            self.fields["department"].initial = teacher.department
            self.fields["qualification"].initial = teacher.qualification
            self.fields["phone"].initial = teacher.phone
            self.fields["courses"].initial = Course.objects.filter(teachers=teacher)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exclude(id=self.teacher.user.id).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exclude(id=self.teacher.user.id).exists():
            raise forms.ValidationError("Email already exists.")
        return email
