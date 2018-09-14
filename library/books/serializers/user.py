from rest_framework import serializers
from ..models.user import Reader


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ('first_name', 'last_name', 'birth_date', 'address', 'telephone')
        read_only_fields = ('PESEL')