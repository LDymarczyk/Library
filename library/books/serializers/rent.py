from rest_framework import serializers
from ..models.rent import Rent


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = ('rent_id', 'start_date', 'end_date', 'book', 'library')