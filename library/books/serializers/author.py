from rest_framework import serializers
from ..models.author import Author
from rest_framework.exceptions import ValidationError
from datetime import date


class AuthorSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        birth_year = attrs.get('birth_year')
        death_year = attrs.get('death_year')
        if birth_year>death_year:
            raise ValidationError("People can't die before their birth. Wrong birth/death years.")
        if death_year-birth_year<10:
            raise ValidationError("Some people are geniuses, but I don't think they can write a book before they are 10.")
        return attrs

    def validate_first_name(self, first_name):
        if len(first_name)<4:
            raise ValidationError("First name must be longer than 3 letters.")
        if len(first_name)>=57:
            raise ValidationError("The longest name in the world is: RhoshandiatellyneshiaunneveshenkKoyaanisquatsiuth (57 letters), please enter some shorter.")
        return first_name

    def validate_last_name(self, last_name):
        if len(last_name)<4:
            raise ValidationError("Last name must be longer than 3 letters.")
        if len(last_name)>=57:
            raise ValidationError("Please enter shorter last name.")
        return last_name

    def validate_birth_year(self, birth_year):
        if birth_year<1400:
            raise ValidationError("Birth year must be greater than 1400. Printing was invented in 1450.")
        if birth_year>date.today().year:
            raise ValidationError("Author doesn't born yet.")
        return birth_year

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'birth_year', 'death_year', 'id', 'creator', 'created')
        read_only_field = ('id', 'creator', 'created')
