from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from django import forms


class Form0(forms.Form):
    name = forms.CharField(max_length=22)
    age = forms.IntegerField()
    name = forms.CharField()

    print()
