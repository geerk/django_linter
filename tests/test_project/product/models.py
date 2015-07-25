from datetime import datetime
from django.db import models
from django import forms
from django.contrib import admin

from test_project import settings


class Form1(forms.Form):
    pass


class Form2(forms.ModelForm):
    pass


class Category(models.Model):
    name = models.CharField()

    def __unicode__(self):
        print 'unicode called'
        return '{}'.format(self.id)


class Product(models.Model):
    MATERIAL, EPHEMERAL = range(1, 3)
    TYPE_CHOICES = (
        (MATERIAL, 'Material'),
        (EPHEMERAL, 'Ephemeral'))

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.FloatField()
    modified_at = models.DateTimeField('abc', default=datetime.now)
    ptype = models.SmallIntegerField(choices=TYPE_CHOICES)
    name = models.CharField(max_length=25)
    category_id = models.ForeignKey(Category)

    def __unicode__(self):
        print('unicode called')
        return self.price


class ProductAdmin(admin.ModelAdmin):
    pass

admin.register(ProductAdmin, Product)
