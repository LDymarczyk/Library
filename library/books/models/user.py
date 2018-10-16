from django.db import models
from django.contrib.auth.models import AbstractUser


#todo zmiana nazwy na MyUser aby byl bardziej ogolny plus typ czy reader czy pracownik
class Reader(AbstractUser):
    PESEL = models.BigIntegerField(blank=True, null=True)
    telephone = models.IntegerField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.id, self.first_name, self.last_name)
