from rest_framework import serializers
from ..models.library import Library
from rest_framework.exceptions import ValidationError
import re


class LibrarySerializer(serializers.ModelSerializer):

    # def validator_email(self, email): ##???
    #     if len(email) > 6:
    #         if not re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email):
    #             return 1
    #     return email

    def validator_address(self, address):

        return address

    def validator_name(self, name):
        libraries = Library.objects.all()
        return name

    def validator_phone(self, phone):
        phone_pattern = re.compile('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{3}|\d{3}[-\.\s]??\d{3})')
        if not phone_pattern.match(phone):
            raise ValidationError("Bad phone number")
        return phone

    class Meta:
        model = Library
        fields = ('address', 'phone', 'email', 'name')