"""
Check for nullable text fields in models
"""
from django.db import models


class Product(models.Model):
    """Product"""
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name
