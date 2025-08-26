from django import forms
from .models import Student
from .models import Attendance
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'student_class', 'age', 'profile_pic', 'gender']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
