from rest_framework import serializers
from ..models.user import Reader
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):

    def validate_PESEL(self, PESEL):
        if len(str(PESEL))!=11:
            raise ValidationError("PESEL number must have 11 digits.")
        control_sum = 0
        control_numbers = [1,3,7,9,1,3,7,9,1,3]
        for i in range(11):
            control_sum += int(str(PESEL)[i]) * control_numbers[i]
        if not control_sum % 10:
            raise ValidationError("PESEL number is incorrect.")
        return PESEL

    class Meta:
        model = Reader
        fields = ('first_name', 'last_name', 'birth_date', 'address', 'telephone')
        read_only_fields = ('PESEL',)