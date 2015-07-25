from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from django import forms

from test_project.settings import STATIC_URL
from .models import Product


class Form0(forms.Form):
    name = forms.CharField(max_length=22)
    age = forms.IntegerField()
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(Form0, self).__init__(*args, **kwargs)
        p = Product.objects.get(id=1)
