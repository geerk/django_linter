"""
Check for presense of __unicode__ method in models
"""
from django.db import models


class Product(models.Model):
    """Product"""
    name = models.CharField(max_length=255)
