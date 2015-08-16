"""
Check for calling reverse in get_absolute_url method
"""
from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
    name = models.CharField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=(self.name,))


class Product(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/products/%s' % self.name
