from rest_framework import serializers
from ..models.author import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'birth_year', 'death_year', 'creator', 'created')
        read_only_field = ('id', 'creator')