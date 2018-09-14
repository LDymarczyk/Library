from django.db import models
from .user import Reader


class Author(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    creator = models.ForeignKey(Reader, on_delete=models.SET_NULL, editable=False, null=True, blank=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'books'

    def create(self, validated_data):
        return Author.object.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birth_year = validated_data.get('birth_year', instance.birth_year)
