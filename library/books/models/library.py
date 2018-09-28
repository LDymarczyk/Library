from django.db import models
from .user import Reader


class Library(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(Reader, editable=False, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)
