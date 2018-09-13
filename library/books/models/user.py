from django.db import models
from django.contrib.auth.models import AbstractUser


class Reader(AbstractUser):
    PESEL = models.IntegerField(blank=True, null=True)
    telephone = models.IntegerField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        app_label = 'books'
