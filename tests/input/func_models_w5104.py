"""
Check that related fields do not contain _id prefix
"""
from django.db import models


class Category(models.Model):
    """Category"""
    name = models.CharField()

    def __unicode__(self):
        return self.name


class Product(models.Model):
    """Product"""
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name
