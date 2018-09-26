from rest_framework import serializers
from ..models.library import Library


class LibrarySerializer(serializers.ModelSerializer):

    def validator_email(self, email):

        return email

    def validator_address(self, address):

        return address

    def validator_address(self, name):

        return name

    def validator_telephone(self, telephone):

        return telephone

    class Meta:
        model = Library
        fields = ('address', 'telephone', 'email', 'name')