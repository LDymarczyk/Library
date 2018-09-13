from django.db import models
from .user import User


class Author(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, editable=False)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    birth_year = models.IntegerField(MinValueValidator=1500)
    death_year = models.IntegerField(MinValueValidator=1500)