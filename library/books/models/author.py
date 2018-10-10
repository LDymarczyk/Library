from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from .user import Reader


class Author(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    edited = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey('Reader', on_delete=models.SET_NULL, editable=False, null=True, blank=True)
    editor = models.ForeignKey(Reader, related_name='author_editor', editable=False, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @staticmethod
    def add_fullname(queryset):
        queryset = queryset.annotate(fullname=Concat('first_name', Value(' '), "last_name"))
        return queryset

    def get_birth_year(self):
        return self.birth_year

    def get_death_year(self):
        return self.death_year

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_full_name(self):
        return self.first_name+" "+self.last_name
