from rest_framework import serializers
from ..models.library import Library


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ('address', 'telephone', 'email', 'name')