"""
Check use of datetime.now instead of auto_now
"""
from datetime import datetime
from django.db import models


class Product(models.Model):
    """Product"""
    name = models.CharField(max_length=255)
    modified = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name
