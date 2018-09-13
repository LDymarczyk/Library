from django.db import models
from .user import Reader


class Author(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(Reader, on_delete=models.SET_NULL, editable=False, null=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    birth_year = models.IntegerField()
    death_year = models.IntegerField()

    class Meta:
        app_label = 'books'
