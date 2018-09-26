from rest_framework import serializers
from ..models.book import Book


class BookSerializer(serializers.ModelSerializer):

    def validate_title(self, title):
        return title

    def validate_ISBN(self, ISBN):
        return ISBN

    def validate_publication_date(self, publication_date):
        return publication_date

    class Meta:
        model = Book
        fields = ('title', 'author', 'ISBN', 'genre', 'edition', 'amount', 'publication_date', 'publishing_house',
                  'language', 'status', 'library', 'creator')

