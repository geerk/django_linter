"""
Check for form field redefinition
"""
from django import forms


class Form0(forms.Form):
    name = forms.CharField(max_length=22)
    age = forms.IntegerField()
    name = forms.CharField()
