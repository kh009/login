from django import forms
from .models import *


class WeekSelectForm(forms.Form):
    week_number = forms.IntegerField()


