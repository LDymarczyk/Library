from rest_framework import serializers
from ..models.book import Book
from rest_framework.exceptions import ValidationError



class BookSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        amount = attrs.get("amount")
        status = attrs.get("status")
        if amount==0 and status==True:
            raise ValidationError("Status of book can't be True if there are no books.")
        return attrs

    def validate_title(self, title):
        if len(title)>100:
            raise ValidationError("Title must have maximum 100 characters.")
        return title

    def validate_ISBN(self, ISBN):
        if len(str(ISBN))not in (10, 13):
            raise ValidationError("ISBN number must have exactly 10 or 13 digits.")
        return ISBN

    def validate_publication_date(self, publication_date):
        if publication_date<1450:
            raise ValidationError("Publication date must be greater than 1450. Printing was invented in 1450.")
        return publication_date

    class Meta:
        model = Book
        fields = ('title', 'author', 'ISBN', 'genre', 'edition', 'amount', 'publication_date', 'publishing_house',
                  'language', 'status', 'library', 'creator')

