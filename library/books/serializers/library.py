from rest_framework import serializers
from ..models.library import Library
import re
from rest_framework.exceptions import ValidationError


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

    def validator_telephone(self, telephone):

        return telephone

    class Meta:
        model = Library
        fields = ('address', 'telephone', 'email', 'name')