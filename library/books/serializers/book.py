from rest_framework import serializers
from ..models import Book, Author
from ..models.book import get_genre
from datetime import date
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
        if publication_date>date.today().year:
            raise ValidationError("This book will be publish in the future.")
        return publication_date

    # def validate_genre(self, genre):
    #     genres = get_genre()
    #     is_valid = False
    #     for i in genres:
    #         if genre == i:
    #             is_valid = True
    #     if not is_valid:
    #         raise ValidationError("Genre is not in base.")


    # def validate_author(self, author):
    #     authors = Author.objects.all()
    #     for i in range(len(authors)):
    #         if authors[i].pk!=author:
    #             raise ValidationError("Author does not exist!")


    class Meta:
        model = Book
        fields = ('title', 'author', 'ISBN', 'genre', 'edition', 'amount', 'publication_date', 'publishing_house',
                  'language', 'status', 'library', 'creator')

