from django import forms
from .models import *


class StudentForm(forms.Form):
    className = forms.CharField(max_length=20, initial='')
    studentID = forms.CharField(max_length=8, initial='')
    name = forms.CharField(max_length=5, initial='', required=False)
    password = forms.CharField(max_length=255, initial='', required=False)
    email = forms.EmailField(max_length=100, initial='', required=False)


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('name', 'studentID')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': '姓名',
            'studentID': '學號'
        }


# forms.py

class AbsenceForm(forms.Form):
    course_seat = forms.ModelChoiceField(
        queryset=Course_seat.objects.all(), label='选择学生选课记录')
    is_absent = forms.BooleanField(label='缺席', required=False)
    # course = forms.ModelChoiceField(queryset=Course.objects.all(), label='选择课程')


class WeekSelectForm(forms.Form):
    week_number = forms.IntegerField()


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
