from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True)
    price = models.FloatField()
