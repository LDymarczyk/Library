from rest_framework import serializers
from ..models.library import Library
from rest_framework.exceptions import ValidationError


class LibrarySerializer(serializers.ModelSerializer):

    def validate_name(self, name):
        libraries = Library.objects.all()
        for library in libraries:
            if library.name==name:
                raise ValidationError("This name already exist in our base.")
        return name

    def validate_phone(self, phone):
        # raise ValidationError("test")
        numbers='1234567890'
        is_valid=True
        for number in phone:
            if number not in numbers:
                is_valid=False
        if len(phone)!=9:
            is_valid=False
        if not is_valid:
            raise ValidationError("Entered bad phone number.")
        return phone

    class Meta:
        model = Library
        fields = ('address', 'phone', 'email', 'name')