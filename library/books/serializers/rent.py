from rest_framework import serializers
from ..models.rent import Rent


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = ('start_date', 'end_date', 'book', 'reader', 'library')
        read_only_field = ('creator', 'id')