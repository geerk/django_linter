from datetime import datetime
from django.db import models


class Category(models.Model):
    name = models.CharField()

    def __unicode__(self):
        return '{}'.format(self.id)


class Product(models.Model):
    MATERIAL, EPHEMERAL = range(1, 3)
    TYPE_CHOICES = (
        (MATERIAL, 'Material'),
        (EPHEMERAL, 'Ephemeral'))

    name = models.CharField(max_length=25)
    description = models.TextField(null=True)
    price = models.FloatField()
    modified_at = models.DateTimeField('abc', default=datetime.now)
    ptype = models.SmallIntegerField(choices=TYPE_CHOICES)
    category_id = models.ForeignKey(Category)

    def __unicode__(self):
        return self.price