from django.db import models
from .user import User


class Library(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_lenght=200)
    telephone = models.IntegerField()
    email = models.CharField(max_lenght=100)
    name = models.CharField(max_lenght=100)