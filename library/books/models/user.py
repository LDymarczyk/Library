from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    PESEL = models.IntegerField()
    telephone = models.IntegerField()
    birth_date = models.DateField()
    address = models.CharField(max_length=200)